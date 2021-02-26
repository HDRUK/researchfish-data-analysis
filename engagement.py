import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from functools import reduce

PATH_TO_NP_2019_AWARD_REFS = 'hdruk_groups/national_priority_group_award_refs.json'
PATH_TO_COMM_2019_AWARD_REFS = 'hdruk_groups/community_group_award_refs.json'
PATH_TO_ACT_2019_AWARD_REFS = 'hdruk_groups/hdruk_activities_award_refs.json'
PATH_TO_RESEARCHFISH_2019_DATA = 'datasets/hdruk_researchfish_data_2019.xlsx'


def read_workbook(file_path):
    
    workbook = pd.read_excel(file_path, sheet_name = None) # read all sheets
    
    return workbook


def read_json(path_to_json):
    
    with open(path_to_json) as fp:
        data_dict = json.load(fp)

    return data_dict


def bar_plot(dataframe, x_label, y_lable, x_tick):
    ax = dataframe.plot.bar(figsize = (24, 10), width=0.8, rot = 6)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_lable)
    ax.set_xticklabels(x_tick) #  y_tick title = title_,
    # ax.set_yticks(np.arange(0, max(y_tick)+5, 5))
    plt.show()
    #ax.figure.savefig('outputs/Primary Audience for National priority.png')

class engagement(object):
    def primary_audience_2019(workbook, award_refs_dict):
        ENGAGEMENT_DF = workbook['Engagement']

        engagement_df_np = pd.DataFrame(columns = ENGAGEMENT_DF.columns)

        for key in award_refs_dict:
            for value in award_refs_dict[key]:
                engagement_df_np = engagement_df_np.append(ENGAGEMENT_DF.loc[ENGAGEMENT_DF['Award Reference'] == value])
                engagement_df_np.reset_index(inplace =True, drop =True)
        
        national_p_group = list(award_refs_dict.keys())

        count = 0
        for group in national_p_group:
            
            group_refs = award_refs_dict[group]
            group_df = engagement_df_np[engagement_df_np['Award Reference'].isin(group_refs)]
            national_p_group[count] = [national_p_group[count], group_df]
            count += 1

        # renaming 
        for group in national_p_group:
            group[1]['Award Reference'] = group[0]


        pa_counts = list(award_refs_dict.keys())
        count = 0
        for group in pa_counts:
            group_refs = award_refs_dict[group]
            count_df = pd.DataFrame(national_p_group[count][1]['Primary Audience*'].value_counts()).reset_index()
            count_df.columns = ['primary_audiecce', pa_counts[count]]
            pa_counts[count] = [pa_counts[count], count_df]
            count += 1

        # # merging all DataFrames together
        pdList = [group[1] for group in pa_counts]
        df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['primary_audiecce'],
                                                how='outer'), pdList)
       
        bar_plot(df_merged, "Primary Audience", "Count", df_merged['primary_audiecce']) # title and ytick labels needs to be added




def main():

    np_2019_award_refs_dict = read_json(PATH_TO_NP_2019_AWARD_REFS)
    comm_2019_award_refs_dict = read_json(PATH_TO_COMM_2019_AWARD_REFS)
    act_2019_award_refs_dict = read_json(PATH_TO_ACT_2019_AWARD_REFS)

    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)


    # Primary Audience of National Priority Group
    engagement.primary_audience_2019(workbook = rf_2019_wb, award_refs_dict = np_2019_award_refs_dict)
    # Primary Audience of Community Group Group
    engagement.primary_audience_2019(rf_2019_wb, comm_2019_award_refs_dict)
    # Primary Audience of Activities Group
    engagement.primary_audience_2019(rf_2019_wb, act_2019_award_refs_dict)


if '__main__' == __name__:
    main()
