import requests_html, json, time
import PySimpleGUI as sg
import pandas as pd
from pandas import DataFrame
import numpy as np
from pathlib import Path
from taxontabletools.taxontable_manipulation import strip_metadata
from taxontabletools.taxontable_manipulation import collect_metadata
from taxontabletools.taxontable_manipulation import add_metadata

def gbif_parent_check(phylum_name, taxon_name, taxonomy_check):

    # taxon_name = "Aturidae"
    # taxon_level = "Family"
    ## create an html session
    time.sleep(0.1)
    with requests_html.HTMLSession() as session:
        ## generate html request name
        request_name = '%20'.join(taxon_name.split(' '))
        ## request that name
        r = session.get("https://api.gbif.org/v1/species/match?verbose=true&name=" + request_name + "&limit=1")
        ## parse json
        res = json.loads(r.text)

        gbif_result = []

        if 'note' in res.keys():
            if "Multiple equal matches" in res['note']:
                empty = True
                for match in res["alternatives"]:
                    try:
                        match_phylum = match["phylum"]
                    except:
                        match_phylum = "nan"
                    if phylum_name == match_phylum:
                        try:
                            for taxon_level in taxonomy_check:
                                    gbif_result.append(match[taxon_level.lower()])
                            return gbif_result
                            break
                        except:
                            gbif_result.append("")
                            return gbif_result
                            break
            else:
                for taxon_level in taxonomy_check:
                    try:
                        gbif_result.append(res[taxon_level.lower()])
                    except:
                        gbif_result.append("")
                return gbif_result
        else:
            gbif_result.append("")
            return gbif_result

        if empty == True:
            return "ERROR"

def gbif_check_taxonomy(TaXon_table_xlsx, path_to_outdirs):

    ## load TaxonTable
    TaXon_table_xlsx = Path(TaXon_table_xlsx)
    TaXon_table_df = pd.read_excel(TaXon_table_xlsx).fillna('')
    TaXon_table_df_metadata = collect_metadata(TaXon_table_df)
    TaXon_table_df = strip_metadata(TaXon_table_df)


    taxon_levels = ["Phylum","Class","Order","Family","Genus","Species"]
    OTUs_list = TaXon_table_df["ID"].values.tolist()

    taxonomy_check_dict = {}

    ############################################################################
    ## create the progress bar window
    layout = [[sg.Text('Progress bar')],
              [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')],
              [sg.Cancel()]]
    window_progress_bar = sg.Window('Progress bar', layout, keep_on_top=True)
    progress_bar = window_progress_bar['progressbar']
    progress_update = 0
    progress_increase = 1000 / len(OTUs_list)
    ############################################################################

    for OTU in TaXon_table_df[["Phylum","Class","Order","Family","Genus","Species"]].fillna("").values.tolist():
        for i, taxonomy in enumerate(OTU):
            if taxonomy == "":
                phylum_name = OTU[0]
                taxon_name = OTU[i-1]
                taxonomy_check = taxon_levels[0: i]
                result = gbif_parent_check(phylum_name, taxon_name, taxonomy_check)
                query = OTU[0: i]
                if (query != result and result != "ERROR"):
                    if len(query) != 6:
                        add = 6 - len(query)
                        query = query + [''] * add
                    if len(result) != 6:
                        add = 6 - len(result)
                        result = result + [''] * add
                    query = ",".join(query)
                    taxonomy_check_dict[query] = result
                break

            elif i == 5:
                phylum_name = OTU[0]
                taxon_name = OTU[5]
                taxonomy_check = taxon_levels
                result = gbif_parent_check(phylum_name, taxon_name, taxonomy_check)
                if (OTU != result and result != "ERROR"):
                    query = ",".join(OTU)
                    taxonomy_check_dict[query] = result

        ############################################################################
        event, values = window_progress_bar.read(timeout=10)
        if event == 'Cancel'  or event is None:
            window_progress_bar.Close()
            raise RuntimeError
        # update bar with loop value +1 so that bar eventually reaches the maximum
        progress_update += progress_increase
        progress_bar.UpdateBar(progress_update)
        ############################################################################

    window_progress_bar.Close()

    TaXon_table_list = []

    for OTU in TaXon_table_df.fillna("").values.tolist():
        taxonomy = OTU[1:7]
        search_key = ','.join(taxonomy)
        if (search_key in taxonomy_check_dict.keys() and taxonomy_check_dict[search_key] != ['']*6):
            replacement_taxonomy = taxonomy_check_dict[search_key]
            replacement_OTU = [OTU[0]] + replacement_taxonomy + OTU[7:]
            TaXon_table_list.append(replacement_OTU)
        else:
            TaXon_table_list.append(OTU)

    file_name = TaXon_table_xlsx.stem
    output_name = Path(str(path_to_outdirs) + "/TaXon_tables/" + file_name + "_gbif" + ".xlsx")
    df_new = pd.DataFrame(TaXon_table_list, columns=(TaXon_table_df.columns.values.tolist()))

    ## replace missing taxonomy in the new dataframe with a >FLAG< placeholder
    taxonomy_list = df_new[["ID", "Phylum", "Class", "Order", "Family", "Genus", "Species"]].values.tolist()
    answer = "NO"
    for entry in taxonomy_list:
        if "" in entry:
            taxonomy = entry[1:]
            OTU = entry[0]
            n_nan = taxonomy.count("")
            if 6 - taxonomy.index("") != n_nan:
                answer = sg.Popup("Internally missing taxonomy found!\nReplacing cases of missing taxonomy with a >FLAG< placeholder.\nPlease adjust the taxonomy in Excel.")
                break
    if answer == 'OK':
        new_df_list = []
        for row in df_new.values.tolist():
            entry = row[0:7]
            if "" in entry:
                taxonomy = entry[1:]
                OTU = entry[0]
                n_nan = taxonomy.count("")
                if 6 - taxonomy.index("") != n_nan:
                    for item in [i for i,x in enumerate(entry) if x == ""]:
                        row[item] = ">FLAG<"
            row = ['' if x=='' else x for x in row]
            new_df_list.append(row)
        column_names = df_new.columns.tolist()
        df_new = pd.DataFrame(new_df_list, columns=column_names)

    ## add already existing metadata back to the df
    if len(TaXon_table_df_metadata.columns) != 1:
        df_new = add_metadata(df_new, TaXon_table_df_metadata)

    ## write dataframe
    df_new.to_excel(output_name, index=False)

    change_log_list = []
    for key, value in taxonomy_check_dict.items():
        change_log_list.append(["Input:"] + key.split(","))
        change_log_list.append(["Gbif:"] + value)

    change_log_df = pd.DataFrame(change_log_list, columns=(["Change"] + taxon_levels))
    change_log_name = Path(str(path_to_outdirs) + "/GBIF/" + file_name + "_gbif_log" + ".xlsx")
    change_log_df = pd.DataFrame(change_log_list, columns=(["Change"] + taxon_levels))
    change_log_df.to_excel(change_log_name, sheet_name = 'TaXon table', index=False)

    closing_text = "Taxon table is found under:\n" + '/'.join(str(output_name).split("/")[-4:]) + "\n\n" + "Log file is found under:\n" + '/'.join(str(change_log_name).split("/")[-4:])
    sg.Popup(closing_text, title="Finished", keep_on_top=True)

    from taxontabletools.create_log import ttt_log
    ttt_log("gbif check", "processing", TaXon_table_xlsx.name, output_name.name, "nan", path_to_outdirs)
