import pandas as pd
import numpy as np
from skbio.diversity import beta_diversity
from skbio.stats.ordination import cca
from skbio.stats.distance import anosim
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from pathlib import Path
import PySimpleGUI as sg
import os, webbrowser
from itertools import combinations
from taxontabletools.taxontable_manipulation import strip_metadata

def CCA_analysis(TaXon_table_xlsx, meta_data_to_test, taxonomic_level, width, height, cca_scatter_size, path_to_outdirs, template, font_size, color_discrete_sequence):

    ## load TaxonTable
    TaXon_table_xlsx = Path(TaXon_table_xlsx)
    TaXon_table_df = pd.read_excel(TaXon_table_xlsx).fillna('unidentified')
    TaXon_table_df = strip_metadata(TaXon_table_df)

    Meta_data_table_xlsx = Path(str(path_to_outdirs) + "/" + "Meta_data_table" + "/" + TaXon_table_xlsx.stem + "_metadata.xlsx")
    Meta_data_table_df = pd.read_excel(Meta_data_table_xlsx, header=0).fillna("nan")

    IDs_list = TaXon_table_df["ID"].values.tolist()
    TaXon_table_samples = TaXon_table_df.columns.tolist()[10:]

    metadata_list = Meta_data_table_df[meta_data_to_test].values.tolist()
    metadata_loc = Meta_data_table_df.columns.tolist().index(meta_data_to_test)

    ## drop samples with metadata called nan (= empty)
    drop_samples = [i[0] for i in Meta_data_table_df.values.tolist() if i[metadata_loc] == "nan"]

    if drop_samples != []:
        ## filter the TaXon table
        TaXon_table_df = TaXon_table_df.drop(drop_samples, axis=1)
        TaXon_table_samples = TaXon_table_df.columns.tolist()[10:]
        ## also remove empty OTUs
        row_filter_list = []
        for row in TaXon_table_df.values.tolist():
            reads = set(row[10:])
            if reads != {0}:
                row_filter_list.append(row)
        columns = TaXon_table_df.columns.tolist()
        TaXon_table_df = pd.DataFrame(row_filter_list, columns=columns)
        Meta_data_table_df = pd.DataFrame([i for i in Meta_data_table_df.values.tolist() if i[0] not in drop_samples], columns=Meta_data_table_df.columns.tolist())
        Meta_data_table_samples = Meta_data_table_df['Samples'].tolist()

    ## create a y axis title text
    taxon_title = taxonomic_level.lower()

    ## adjust taxonomic level if neccessary
    if taxonomic_level in ["ASVs", "ESVs", "OTUs", "zOTUs"]:
        taxon_title = taxonomic_level
        taxonomic_level = "ID"

    # check for presence absence data
    # otherwise abort and print error message
    for i in Meta_data_table_df[meta_data_to_test]:
        if type(i) != int:
            sg.Popup("Please use categorial numbers (ints) as meta data!", title=("Error"))
            raise RuntimeError

    # check if the meta data differs
    if len(set(Meta_data_table_df[meta_data_to_test])) == len(Meta_data_table_df['Samples'].tolist()):
        sg.Popup("The meta data is unique for all samples. Please adjust the meta data table!", title=("Error"))
        raise RuntimeError

    # check if the meta data differs
    if len(set(Meta_data_table_df[meta_data_to_test])) == 1:
        sg.Popup("The meta data is similar for all samples. Please adjust the meta data table!", title=("Error"))
        raise RuntimeError

    # check for empty samples and later remove them from the dataframe
    # otherwise abort and print error message
    TaXon_table_samples = TaXon_table_df.columns.tolist()[10:]
    empty_samples_list = []
    for sample in TaXon_table_samples:
        empty_sample_test = set(TaXon_table_df[sample].values.tolist())
        if empty_sample_test == {0}:
            empty_samples_list.append(sample)
    if empty_samples_list != []:
        sg.Popup("Please remove empty samples first!", title=("Error"))
        raise RuntimeError

    Meta_data_table_samples = Meta_data_table_df['Samples'].tolist()

    if sorted(TaXon_table_samples) == sorted(Meta_data_table_samples):
        ## create title
        textbox = meta_data_to_test + ", " + taxon_title

        ## collect samples
        samples = Meta_data_table_samples

        ## create metadata list
        metadata_list = Meta_data_table_df[meta_data_to_test].values.tolist()

        ## extract the relevant data
        TaXon_table_df = TaXon_table_df[[taxonomic_level] + samples]
        ## define an aggregation function to combine multiple hit of one taxonimic level
        aggregation_functions = {}
        ## define samples functions
        for sample in samples:
            ## 'sum' will calculate the sum of p/a data
            aggregation_functions[sample] = 'sum'
        ## define taxon level function
        aggregation_functions[taxonomic_level] = 'first'
        ## create condensed dataframe
        TaXon_table_df = TaXon_table_df.groupby(TaXon_table_df[taxonomic_level]).aggregate(aggregation_functions)
        if 'unidentified' in TaXon_table_df.index:
            TaXon_table_df = TaXon_table_df.drop('unidentified')

        # transpose the pa table
        df_features = TaXon_table_df[samples].transpose()
        df_features.index = samples
        df_features = df_features.rename_axis("a")

        # create a constrains table from the metadata table
        constrains_list = []
        for col in Meta_data_table_df[["Samples", meta_data_to_test]].values.tolist():
            constrains_list.append(float(col[1]))
        df_constrains = pd.DataFrame(constrains_list, samples, [meta_data_to_test])
        df_constrains.index = samples
        df_constrains = df_constrains.rename_axis("a")

        ordination_result = cca(df_features, df_constrains)
        ordination_result.sample_constraints

        #######################################################################################
        # create window to ask for CCA axis to test
        def slices(list, slice):
            for i in range(0, len(list), slice):
                yield list[i : i + slice]

        # collect the cca proportion explained values
        proportion_explained_list = []
        for i, cca_axis in enumerate(ordination_result.proportion_explained):
            if round(cca_axis* 100, 2) >= 1:
                proportion_explained_list.append("CCA" + str(i+1) + " (" + str(round(cca_axis* 100, 2)) + " %)")

        cca_axis_checkboxes = list(slices([sg.Checkbox(name, key=name, size=(15,1)) for name in proportion_explained_list], 10))

        cca_window_layout = [
                        [sg.Text('Check up to four axes to be displayed')],
                        [sg.Frame(layout = cca_axis_checkboxes, title = '')],
                        [sg.Text('Only axes >= 1 % explained variance are shown')],
                        [sg.CB("Connect categories", default=True, key="draw_mesh")],
                        [sg.Text('')],
                        [sg.Button('Plot', key='Plot')],
                        [sg.Button('Back')],
                        ]

        cca_window = sg.Window('CCA axis', cca_window_layout, keep_on_top=True)

        while True:
            event, values = cca_window.read()

            draw_mesh = values["draw_mesh"]

            if event is None or event == 'Back':
                break

            if event == 'Plot':

                ## create a subfolder for better sorting and overview
                dirName = Path(str(path_to_outdirs) + "/" + "CCA_plots" + "/" + TaXon_table_xlsx.stem + "/")
                if not os.path.exists(dirName):
                    os.mkdir(dirName)

                # collect the CCA axis values
                axis_to_plot = [key for key,value in values.items() if value == True and "CCA" in key]
                # pass on only if two CCA axes were checked
                if len(axis_to_plot) == 2:
                    cat1 = axis_to_plot[1].split()[0]
                    cat2 = axis_to_plot[0].split()[0]

                    df_cca = ordination_result.samples[[cat1, cat2]]
                    df_cca.insert(2, "Samples", Meta_data_table_df["Samples"].values.tolist(), True)
                    df_cca.insert(3, "Metadata", [str(value) for value in Meta_data_table_df[meta_data_to_test].values.tolist()], True)

                    if draw_mesh == True:
                        combinations_list =[]
                        for metadata in df_cca["Metadata"]:
                            ## collect all entries for the respective metadata
                            arr = df_cca.loc[df_cca['Metadata'] == metadata][[cat1, cat2, "Metadata", "Samples"]].to_numpy()
                            ## create a df for all possible combinations using itertools combinations
                            for entry in list(combinations(arr, 2)):
                                combinations_list.append(list(entry[0]))
                                combinations_list.append(list(entry[1]))
                        ## create a dataframe to draw the plot from
                        df = pd.DataFrame(combinations_list)
                        df.columns = [cat1, cat2, "Metadata", "Samples"]

                        fig = px.scatter(df, x=cat1, y=cat2, color="Metadata", text="Samples", title=textbox, color_discrete_sequence=color_discrete_sequence)
                        fig.update_traces(marker_size=int(cca_scatter_size), mode="markers+lines")
                        fig.update_layout(height=int(height), width=int(width), template=template, showlegend=True, font_size=font_size, title_font_size=font_size)
                        fig.update_xaxes(title=axis_to_plot[1])
                        fig.update_yaxes(title=axis_to_plot[0])

                    else:
                        fig = px.scatter(df, x=cat1, y=cat2, color="Metadata", text="Samples", title=textbox, color_discrete_sequence=color_discrete_sequence)
                        fig.update_traces(marker_size=int(cca_scatter_size), mode="markers")
                        fig.update_layout(height=int(height), width=int(width), template=template, showlegend=True, font_size=font_size, title_font_size=font_size)
                        fig.update_xaxes(title=axis_to_plot[1])
                        fig.update_yaxes(title=axis_to_plot[0])

                    ## define output files
                    output_pdf = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + ".pdf")
                    output_html = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + ".html")
                    output_xlsx = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + ".xlsx")

                    fig.write_image(str(output_pdf))
                    fig.write_html(str(output_html))
                    ordination_result.samples[[cat1, cat2]].to_excel(output_xlsx)

                    ## ask to show file
                    answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
                    if answer == "Yes":
                        webbrowser.open('file://' + str(output_html))

                    ## print closing text
                    closing_text = "\n" + "CCA plots are found in: " + str(path_to_outdirs) + "/CCA_plots/"
                    sg.Popup(closing_text, title="Finished", keep_on_top=True)

                    ## write log file
                    from taxontabletools.create_log import ttt_log
                    ttt_log("cca analysis", "analysis", TaXon_table_xlsx.name, output_pdf.name, meta_data_to_test, path_to_outdirs)
                    break


                elif len(axis_to_plot) == 3:
                    cat1 = axis_to_plot[0].split()[0]
                    cat2 = axis_to_plot[1].split()[0]
                    cat3 = axis_to_plot[2].split()[0]

                    df_cca = ordination_result.samples[[cat1, cat2, cat3]]
                    df_cca.insert(3, "Samples", Meta_data_table_df["Samples"].values.tolist(), True)
                    df_cca.insert(4, "Metadata", [str(value) for value in Meta_data_table_df[meta_data_to_test].values.tolist()], True)

                    ## check if lines are to be drawn between the dots
                    if draw_mesh == True:
                        combinations_list =[]
                        for metadata in df_cca["Metadata"]:
                            ## collect all entries for the respective metadata
                            arr = df_cca.loc[df_cca['Metadata'] == str(metadata)][[cat1, cat2, cat3, "Metadata", "Samples"]].to_numpy()
                            ## create a df for all possible combinations using itertools combinations
                            for entry in list(combinations(arr, 2)):
                                combinations_list.append(list(entry[0]))
                                combinations_list.append(list(entry[1]))
                        ## create a dataframe to draw the plot from
                        df = pd.DataFrame(combinations_list)
                        df.columns = [cat1, cat2, cat3, "Metadata", "Samples"]
                        ## draw the plot
                        fig = px.scatter_3d(df, x=cat1, y=cat2, z=cat3, color="Metadata", text="Samples", title=textbox, color_discrete_sequence=color_discrete_sequence)
                        fig.update_traces(marker_size=int(cca_scatter_size), mode="markers+lines", line=dict(width=0.5))
                        fig.update_layout(height=int(height), width=int(width), title=textbox, template=template, showlegend=True, font_size=font_size, title_font_size=font_size)
                        fig.update_layout(scene = dict(xaxis_title=axis_to_plot[0],yaxis_title=axis_to_plot[1],zaxis_title=axis_to_plot[2]))
                    else:
                        fig = px.scatter_3d(df_cca, x=cat1, y=cat2, z=cat3, color="Metadata", text="Samples", color_discrete_sequence=color_discrete_sequence)
                        fig.update_traces(marker_size=int(cca_scatter_size), mode="markers")
                        fig.update_layout(height=int(height), width=int(width), template=template, title=textbox, showlegend=True, font_size=font_size, title_font_size=font_size)
                        fig.update_layout(scene = dict(xaxis_title=axis_to_plot[0],yaxis_title=axis_to_plot[1],zaxis_title=axis_to_plot[2]))

                    ## define output files
                    output_pdf = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + "_3d.pdf")
                    output_html = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + "_3d.html")
                    output_xlsx = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + "_3d.xlsx")

                    fig.write_image(str(output_pdf))
                    fig.write_html(str(output_html))
                    ordination_result.samples[[cat1, cat2]].to_excel(output_xlsx)

                    ## ask to show file
                    answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
                    if answer == "Yes":
                        webbrowser.open('file://' + str(output_html))

                    ## print closing text
                    closing_text = "\n" + "CCA plots are found in: " + str(path_to_outdirs) + "/CCA_plots/"
                    sg.Popup(closing_text, title="Finished", keep_on_top=True)

                    ## write to log file
                    from taxontabletools.create_log import ttt_log
                    ttt_log("cca analysis", "analysis", TaXon_table_xlsx.name, output_pdf.name, meta_data_to_test, path_to_outdirs)
                    break

                else:
                    sg.Popup("Please choose not more than 3 CCA axes", title="Error", keep_on_top=True)

            if event == 'Plot matrix':
                if len(proportion_explained_list) >= 4:

                    ## create a subfolder for better sorting and overview
                    dirName = Path(str(path_to_outdirs) + "/" + "CCA_plots" + "/" + TaXon_table_xlsx.stem + "/")
                    if not os.path.exists(dirName):
                        os.mkdir(dirName)

                    df_cca = ordination_result.samples[["CCA1", "CCA2", "CCA3", "CCA4"]]
                    df_cca.insert(4, "Sample", Meta_data_table_df["Samples"].values.tolist(), True)
                    df_cca.insert(5, "Metadata", [str(value) for value in Meta_data_table_df[meta_data_to_test].values.tolist()], True)

                    fig = make_subplots(rows=4, cols=4)
                    ########### 1 ###########
                    fig.add_trace(go.Scatter(),row=1, col=1)
                    fig.update_layout(template=template, font_size=font_size, title_font_size=font_size)
                    text = "CCA1 (" + str(round(ordination_result.proportion_explained["CCA1"]* 100, 2)) + " %)"
                    fig.add_annotation(text=text, showarrow=False)
                    fig.update_xaxes(showticklabels=False, showgrid=False)
                    fig.update_yaxes(showticklabels=False, showgrid=False)
                    ########### 2 ###########
                    df = df_cca[["CCA1", "CCA2", "Metadata", "Sample"]]
                    for metadata in set(metadata_list):
                        df_metadata = df[df['Metadata'] == str(metadata)]
                        #fig = px.scatter(df_cca, x="CCA1", y="CCA2", , )
                        fig.add_trace(go.Scatter(   x=df_metadata["CCA1"].values.tolist(),
                                                    y=df_metadata["CCA2"].values.tolist(),
                                                    mode='markers',
                                                    name=metadata,
                                                    text=df_metadata["Sample"].values.tolist()),row=1, col=2)
                    ########### 3 ###########
                    df = df_cca[["CCA1", "CCA3", "Metadata", "Sample"]]
                    for metadata in set(metadata_list):
                        df_metadata = df[df['Metadata'] == str(metadata)]
                        #fig = px.scatter(df_cca, x="CCA1", y="CCA2", , )
                        fig.add_trace(go.Scatter(   x=df_metadata["CCA1"].values.tolist(),
                                                    y=df_metadata["CCA3"].values.tolist(),
                                                    mode='markers',
                                                    name=metadata,
                                                    showlegend=False,
                                                    text=df_metadata["Sample"].values.tolist()),row=1, col=3)
                    ########### 4 ###########
                    df = df_cca[["CCA1", "CCA4", "Metadata", "Sample"]]
                    for metadata in set(metadata_list):
                        df_metadata = df[df['Metadata'] == str(metadata)]
                        fig.add_trace(go.Scatter(   x=df_metadata["CCA1"].values.tolist(),
                                                    y=df_metadata["CCA4"].values.tolist(),
                                                    mode='markers',
                                                    name=metadata,
                                                    showlegend=False,
                                                    text=df_metadata["Sample"].values.tolist()),row=1, col=4)
                        fig.update_traces(marker_size=int(cca_scatter_size), mode="markers")
                        fig.update_xaxes(showgrid=False,row=1, col=4)
                        fig.update_yaxes(showgrid=False,row=1, col=4)
                    ########### 5 ###########
                    fig.add_trace(go.Scatter(),row=2, col=2)
                    fig.update_layout(template=template, font_size=font_size, title_font_size=font_size)
                    text = "CCA2 (" + str(round(ordination_result.proportion_explained["CCA2"]* 100, 2)) + " %)"
                    fig.add_annotation(text=text, showarrow=False, row=2, col=2)
                    ########### 6 ###########
                    df = df_cca[["CCA2", "CCA3", "Metadata", "Sample"]]
                    for metadata in set(metadata_list):
                        df_metadata = df[df['Metadata'] == str(metadata)]
                        #fig = px.scatter(df_cca, x="CCA1", y="CCA2", , )
                        fig.add_trace(go.Scatter(   x=df_metadata["CCA2"].values.tolist(),
                                                    y=df_metadata["CCA3"].values.tolist(),
                                                    mode='markers',
                                                    name=metadata,
                                                    showlegend=False,
                                                    text=df_metadata["Sample"].values.tolist()),row=2, col=3)
                    ########### 7 ###########
                    df = df_cca[["CCA2", "CCA4", "Metadata", "Sample"]]
                    for metadata in set(metadata_list):
                        df_metadata = df[df['Metadata'] == str(metadata)]
                        fig.add_trace(go.Scatter(   x=df_metadata["CCA2"].values.tolist(),
                                                    y=df_metadata["CCA4"].values.tolist(),
                                                    mode='markers',
                                                    name=metadata,
                                                    showlegend=False,
                                                    text=df_metadata["Sample"].values.tolist()),row=2, col=4)
                    ########### 8 ###########
                    fig.add_trace(go.Scatter(),row=3, col=3)
                    fig.update_layout(template=template, font_size=font_size, title_font_size=font_size)
                    text = "CCA3 (" + str(round(ordination_result.proportion_explained["CCA3"]* 100, 2)) + " %)"
                    fig.add_annotation(text=text, showarrow=False, row=3, col=3)
                    ########### 9 ###########
                    df = df_cca[["CCA3", "CCA4", "Metadata", "Sample"]]
                    for metadata in set(metadata_list):
                        df_metadata = df[df['Metadata'] == str(metadata)]
                        #fig = px.scatter(df_cca, x="CCA1", y="CCA2", , )
                        fig.add_trace(go.Scatter(   x=df_metadata["CCA3"].values.tolist(),
                                                    y=df_metadata["CCA4"].values.tolist(),
                                                    mode='markers',
                                                    name=metadata,
                                                    showlegend=False,
                                                    text=df_metadata["Sample"].values.tolist()),row=3, col=4)
                    ########### 5 ###########
                    fig.add_trace(go.Scatter(),row=4, col=4)
                    fig.update_layout(template=template, font_size=font_size, title_font_size=font_size)
                    text = "CCA4 (" + str(round(ordination_result.proportion_explained["CCA4"]* 100, 2)) + " %)"
                    fig.add_annotation(text=text, showarrow=False, row=4, col=4)

                    ######################
                    fig.update_xaxes(showline=True, mirror=True, linewidth=1, linecolor='black')
                    fig.update_yaxes(showline=True, mirror=True, linewidth=1, linecolor='black')
                    fig.update_traces(marker_size=int(cca_scatter_size), mode="markers")
                    # finish plot matrix
                    fig.update_layout(height=1000, width=1000, title_text=textbox)

                    ## define output files
                    output_pdf = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + "_matrix.pdf")
                    output_html = Path(str(dirName) + "/" + meta_data_to_test + "_" + taxon_title + "_matrix.html")

                    fig.write_image(str(output_pdf))
                    fig.write_html(str(output_html))

                    ## ask to show file
                    answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
                    if answer == "Yes":
                        webbrowser.open('file://' + str(output_html))

                    ## print closing text
                    closing_text = "\n" + "CCA plots are found in: " + str(path_to_outdirs) + "/CCA_plots/"
                    sg.Popup(closing_text, title="Finished", keep_on_top=True)

                    ## write to log file
                    from taxontabletools.create_log import ttt_log
                    ttt_log("cca analysis", "analysis", TaXon_table_xlsx.name, output_pdf.name, meta_data_to_test, path_to_outdirs)
                    break
                else:
                    sg.Popup("There must be at least 4 CCA axis available to plot the matrix!")

        cca_window.close()

    else:
        sg.PopupError("The sample of both the TaXon table and the metadata table have to match!")











#
