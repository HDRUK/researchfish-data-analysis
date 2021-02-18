import pandas as pd
import numpy as np
import json

PATH_TO_RESEARCHFISH_2018_DATA = 'datasets\hdruk_researchfish_baseline_2018.xlsx'
PATH_TO_RESEARCHFISH_2019_DATA = 'datasets/hdruk_researchfish_data_2019.xlsx'

# HDRUK_COMMUNITY_GROUPS = ['Fellows', 'Sprint Exemplar teams', 'University research teams']

def read_workbook(file_path):
    
    workbook = pd.read_excel(file_path, sheet_name = None) # read all sheets
    
    return workbook


def get_community_group_award_refs(workbook):

    community_group_award_refs_dict = {'Fellows': [], 'Sprint Exemplar teams': [], 'Univerisity research teams': []}

    award_details_df = workbook['Award Details']

    indices = np.zeros(3)
    for award_type in award_details_df['Award Type']:
        if award_type == 'Fellowship':
            community_group_award_refs_dict['Fellows'].append(award_details_df['Award Reference'][indices[0]])
        indices[0] += 1
    for title in award_details_df['Title']:
        if 'Sprint Exemplar' in title:
            community_group_award_refs_dict['Sprint Exemplar teams'].append(award_details_df['Award Reference'][indices[1]])
        indices[1] += 1    
    for ro in award_details_df['RO']:
        if 'Health Data Research UK' not in ro:
            community_group_award_refs_dict['Univerisity research teams'].append(award_details_df['Award Reference'][indices[2]])
        indices[2] += 1

    return community_group_award_refs_dict

def get_national_priority_groups(workbook):

    national_priorities_award_refs_dict = {'Applied Analytics': [], 'Better Care': [], 'Human Phenome': [], 'Understanding Causes of Disease': [],\
                              'Clinical Trials': [], 'Improving Public Health': []
                              }

    award_details_df = workbook['Award Details']

    index = 0
    for title in award_details_df['Title']:
        if title == 'Health Data Research UK: Applied Analytics':
            national_priorities_award_refs_dict['Applied Analytics'].append(award_details_df['Award Reference'][index])
        elif title == 'Health Data Research UK: Better Care':
            national_priorities_award_refs_dict['Better Care'].append(award_details_df['Award Reference'][index])
        elif title == 'Health Data Research UK: Human Phenome':
            national_priorities_award_refs_dict['Human Phenome'].append(award_details_df['Award Reference'][index])
        elif title == 'Health Data Research UK: Understanding Causes of Disease':
            national_priorities_award_refs_dict['Understanding Causes of Disease'].append(award_details_df['Award Reference'][index])
        elif title == 'Health Data Research UK: Clinical Trials':
            national_priorities_award_refs_dict['Clinical Trials'].append(award_details_df['Award Reference'][index])
        elif title == 'Health Data Research UK: Improving Public Health':
            national_priorities_award_refs_dict['Improving Public Health'].append(award_details_df['Award Reference'][index])
        index += 1

    return national_priorities_award_refs_dict


def get_hdruk_activities_award_refs(workbook):

    hdruk_activities_award_refs_dict = {'Central Infrastructure Activities': [], 'Central PPPEI Activities': [], 'Central Training Activities': []}

    award_details_df = workbook['Award Details']

    index = 0
    for title in award_details_df['Title']:
        if title == 'Health Data Research UK central infrastructure activities':
            hdruk_activities_award_refs_dict['Central Infrastructure Activities'].append(award_details_df['Award Reference'][index])
        elif title == 'Health Data Research UK central PPPEI activities':
            hdruk_activities_award_refs_dict['Central PPPEI Activities'].append(award_details_df['Award Reference'][index])
        elif title == 'Health Data Research UK central training activities':
            hdruk_activities_award_refs_dict['Central Training Activities'].append(award_details_df['Award Reference'][index])
        index += 1

    return hdruk_activities_award_refs_dict


def export_dict_as_json(dict, file_path):
    
    with open(file_path, 'w') as fp:
        json.dump(dict, fp, indent=1)
    

def main():

    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)  

    community_group_award_refs_dict = get_community_group_award_refs(rf_2019_wb)
    national_priorities_award_refs_dict = get_national_priority_groups(rf_2019_wb)
    hdruk_activities_award_refs_dict = get_hdruk_activities_award_refs(rf_2019_wb)

    export_dict_as_json(community_group_award_refs_dict, 'hdruk_groups/community_group_award_refs.json')
    export_dict_as_json(national_priorities_award_refs_dict, 'hdruk_groups/national_priority_group_award_refs.json')
    export_dict_as_json(hdruk_activities_award_refs_dict, 'hdruk_groups/hdruk_activities_award_refs.json')


if '__main__' == __name__:
    main()
