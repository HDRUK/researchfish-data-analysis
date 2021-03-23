import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from functools import reduce
from impact import joined_df


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

# bar plot for multi columns
def bar_plot(dataframe, x_label, y_lable, x_tick):
    ax = dataframe.plot.bar(figsize = (24, 10), width=0.8, rot = 6)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_lable)
    ax.set_xticklabels(x_tick) # y_tick title = title_,
    # ax.set_yticks(np.arange(0, max(y_tick)+5, 5))
    plt.show()
    #ax.figure.savefig('outputs/Primary Audience for National priority.png')  # saves the current figure


def stacked_bar_plot(dataframe, X, title, y_tick, y_label):
    '''take a dataFrame name, x, title, y_yick and y lable'''
    ax = dataframe.plot( x = X, 
                        kind = 'barh', 
                        stacked = True, 
                        title = title, 
                        mark_right = True,
                        figsize=(20, 10))
    ax.set_yticklabels(y_tick)
    ax.set_xlabel('Percentage')
    ax.set_ylabel(y_label)
    plt.show()



def stacked_bar_plot_percentage(dataframe, X, title, y_tick):
    # plot a Stacked Bar Chart using matplotlib 
    ax = dataframe.plot( x = X, 
                            kind = 'barh', 
                            stacked = True, 
                            title = title, mark_right = True) 

    df_total = dataframe["Policymakers"] + dataframe["Professional Practitioners"] + dataframe["General Public"] + dataframe["Patients, Cares, Patient Groups"]
    df_rel = dataframe[dataframe.columns[1:]].div(df_total, 0)*100

    for n in df_rel: 
        for i, (cs, ab, pc) in enumerate(zip(dataframe.iloc[:, 1:].cumsum(1)[n],  
                                        dataframe[n], df_rel[n])): 
            plt.text(cs - ab / 2, i, str(np.round(pc, 1)) + '%', va = 'center', ha = 'center', rotation = 20, fontsize = 8)
    ax.set_yticklabels(y_tick)
    ax.set_xlabel('Percentage')
    #ax.set_ylabel(y_label)
    plt.show()
  

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

        # merging all DataFrames together
        pdList = [group[1] for group in pa_counts]
        df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['primary_audiecce'],
                                                how='outer'), pdList)
       
        bar_plot(df_merged, "Primary Audience", "Count", df_merged['primary_audiecce']) # title and ytick labels needs to be added


    def geographical_reach_2019(workbook, award_refs_dict, plot_name):
            ENGAGEMENT_DF = workbook['Engagement']

            engagement_df_gr = pd.DataFrame(columns = ENGAGEMENT_DF.columns)

            for key in award_refs_dict:
                for value in award_refs_dict[key]:
                    print(value)

                    engagement_df_gr = engagement_df_gr.append(ENGAGEMENT_DF.loc[ENGAGEMENT_DF['Award Reference'] == value])
                    engagement_df_gr.reset_index(inplace =True, drop =True)
            
            national_p_group = list(award_refs_dict.keys())

            count = 0
            for group in national_p_group:
                
                group_refs = award_refs_dict[group]
                group_df = engagement_df_gr[engagement_df_gr['Award Reference'].isin(group_refs)]
                national_p_group[count] = [national_p_group[count], group_df]
                count += 1

            # renaming 
            for group in national_p_group:
                group[1]['Award Reference'] = group[0]


            pa_counts = list(award_refs_dict.keys())
            count = 0
            for group in pa_counts:
                group_refs = award_refs_dict[group]
                count_df = pd.DataFrame(national_p_group[count][1]['Geographical Reach*'].value_counts()).reset_index()
                count_df.columns = ['Geographical Reach', pa_counts[count]]
                pa_counts[count] = [pa_counts[count], count_df]
                count += 1

            # merging all DataFrames together
            pdList = [group[1] for group in pa_counts]
            df_merged_ = reduce(lambda  left,right: pd.merge(left,right,on=['Geographical Reach'],
                                                    how='outer'), pdList)
                                                  
            df_merged_= df_merged_.replace(np.nan, 0) # replacing nan with 0
            df_merged_ = df_merged_.T # transposing dataframe
            df_merged_.transpose()
            df_merged_.columns = [''] * len(df_merged_.columns) # delete automatic created columns name
            new_header = df_merged_.iloc[0] #grab the first row for the header
            df_merged_ = df_merged_[1:] #take the data less the header row
            df_merged_.columns = new_header #['National', 'International', 'Regional', 'Local']
            df_merged_['new_index'] = df_merged_.index

            # pie chart for multi columns
            fig, axes = plt.subplots(2, 3, figsize=(24, 12))

            for i, (idx, row) in enumerate(df_merged_.set_index('new_index').iterrows()):
                ax = axes[i // 3, i % 3]
                row = row[row.gt(row.sum() * .01)]
                ax.pie(row, labels=row.index,  autopct='%1.1f%%') # stacolumnrtangle=30,
                ax.set_title(idx)
                ax.figure.savefig(plot_name)  # saves the current figure

            fig.subplots_adjust(wspace=.2)
            plt.show()
            
    def other_audience_2019(workbook, award_refs_dict, labels):
        ENGAGEMENT_SHEET_DF = workbook['Engagement']

        engagement_df = pd.DataFrame(columns = ['Award Reference','Schools', 'Media', 'Policymakers', 'Professional Practitioners',	'General Public',	'Industry/Business', 	'Supporters/Donors', 'Undergraduates', 'Postgraduates',	'Other Audiences',	'Study Participants',	'Patients, Cares, Patient Groups', 'Third Sector',	'No Other Audience' ])
        

        for key in award_refs_dict:
            for value in award_refs_dict[key]:
                engagement_df = engagement_df.append(ENGAGEMENT_SHEET_DF.loc[ENGAGEMENT_SHEET_DF['Award Reference'] == value])
                engagement_df.reset_index(inplace =True, drop =True)
        engagement_df = engagement_df.groupby("Award Reference").agg({'Schools':['sum'], 'Media':['sum'], 'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Industry/Business':['sum'], 'Supporters/Donors':['sum'], 'Undergraduates':['sum'],'Postgraduates':['sum'], 'Other Audiences':['sum'], 'Study Participants':['sum'], 'Patients, Cares, Patient Groups':['sum'],'Third Sector':['sum'], 'No Other Audience':['sum']})
        engagement_df.columns = engagement_df.columns.droplevel(1)

        bar_plot(engagement_df, "Other Audiences for Groups", "Audience Count", labels)

    def other_community_audience_2019(workbook, award_refs_dict, labels):
        ENGAGEMENT_DF = workbook['Engagement']

        engagement_df = pd.DataFrame(columns = ENGAGEMENT_DF.columns)

        for key in award_refs_dict:
            for value in award_refs_dict[key]:
                engagement_df = engagement_df.append(ENGAGEMENT_DF.loc[ENGAGEMENT_DF['Award Reference'] == value])
                engagemet = engagement_df[["Award Reference", 'Geographical Reach*', 'Schools',	'Media', 'Policymakers', 'Professional Practitioners',	'General Public',	'Industry/Business', 	'Supporters/Donors', 'Undergraduates', 'Postgraduates',	'Other Audiences',	'Study Participants',	'Patients, Cares, Patient Groups',	'Third Sector',	'No Other Audience' ]]
                engagemet.reset_index(inplace =True, drop =True)
        
        national_p_group = list(award_refs_dict.keys())

        count = 0
        for group in national_p_group:
            group_refs = award_refs_dict[group]
            group_df = engagemet[engagemet['Award Reference'].isin(group_refs)]
            national_p_group[count] = [national_p_group[count], group_df]
            count += 1

        # renaming 
        for group in national_p_group:
            group[1]['Award Reference'] = group[0]
    
        fellows_df, sprintET_df, university_rt_df  = national_p_group[0][1], national_p_group[1][1], national_p_group[2][1]

        appl_fellows_df = fellows_df.groupby("Award Reference").agg({'Schools':['sum'], 'Media':['sum'], 'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Industry/Business':['sum'], 'Supporters/Donors':['sum'], 'Undergraduates':['sum'],'Postgraduates':['sum'], 'Other Audiences':['sum'], 'Study Participants':['sum'], 'Patients, Cares, Patient Groups':['sum'],'Third Sector':['sum'], 'No Other Audience':['sum']})
        appl_sprintET_df = sprintET_df.groupby("Award Reference").agg({'Schools':['sum'], 'Media':['sum'], 'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Industry/Business':['sum'], 'Supporters/Donors':['sum'], 'Undergraduates':['sum'],'Postgraduates':['sum'], 'Other Audiences':['sum'], 'Study Participants':['sum'], 'Patients, Cares, Patient Groups':['sum'],'Third Sector':['sum'], 'No Other Audience':['sum']})
        appl_university_rt_df = university_rt_df.groupby("Award Reference").agg({'Schools':['sum'], 'Media':['sum'], 'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Industry/Business':['sum'], 'Supporters/Donors':['sum'], 'Undergraduates':['sum'],'Postgraduates':['sum'], 'Other Audiences':['sum'], 'Study Participants':['sum'], 'Patients, Cares, Patient Groups':['sum'],'Third Sector':['sum'], 'No Other Audience':['sum']})
        
        appl_fellows_df.columns = appl_fellows_df.columns.droplevel(1)
        appl_sprintET_df.columns = appl_sprintET_df.columns.droplevel(1)
        appl_university_rt_df.columns = appl_university_rt_df.columns.droplevel(1)
        
        # merging all DataFrames together
        merged_df = pd.concat([appl_fellows_df, appl_sprintET_df, appl_university_rt_df])

        #plottting dataframe
        bar_plot(merged_df, "Other Audiences for Groups", "Audience Count", labels)
    
    
    def impact_of_hdruk_research(workbook, award_refs_dict, plt_tilte, labels):
        '''takes workbook as main input, awards_refs_dict as dictionary, and labels is the label of the bar plot'''
        ENGAGEMENT_SHEET_DF = workbook['Engagement']

        engagement_df = pd.DataFrame(columns = ['Award Reference', 'Policymakers', 'Professional Practitioners', 'General Public',	'Patients, Cares, Patient Groups' ])

        for key in award_refs_dict:
            for value in award_refs_dict[key]:
                engagement_df = engagement_df.append(ENGAGEMENT_SHEET_DF.loc[ENGAGEMENT_SHEET_DF['Award Reference'] == value])
                engagement_df.reset_index(inplace =True, drop =True)

        engagement_df = engagement_df.groupby("Award Reference").agg({'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Patients, Cares, Patient Groups':['sum']})
        engagement_df.columns = engagement_df.columns.droplevel(1)
        engagement_df['Award_Reference_1'] = engagement_df.index
        engagement_df = engagement_df.reindex(['Award_Reference_1','Policymakers','Professional Practitioners', 'General Public', 'Patients, Cares, Patient Groups'], axis=1)
        engagement_df.reset_index(drop=True, inplace=True)
        
        # plot a Stacked Bar Chart using matplotlib 
        stacked_bar_plot_percentage(engagement_df, "Award_Reference_1", plt_tilte, labels)
    
    def impact_of_community_audience_2019(workbook, award_refs_dict, plt_tilte, labels):
            ENGAGEMENT_DF = workbook['Engagement']

            engagement_df = pd.DataFrame(columns = ['Award Reference', 'Policymakers', 'Professional Practitioners', 'General Public',	'Patients, Cares, Patient Groups'])

            for key in award_refs_dict:
                for value in award_refs_dict[key]:
                    engagement_df = engagement_df.append(ENGAGEMENT_DF.loc[ENGAGEMENT_DF['Award Reference'] == value])
                    engagemet = engagement_df[['Award Reference', 'Policymakers', 'Professional Practitioners', 'General Public',	'Patients, Cares, Patient Groups']]
                    engagemet.reset_index(inplace =True, drop =True)
            
            national_p_group = list(award_refs_dict.keys())

            count = 0
            for group in national_p_group:
                group_refs = award_refs_dict[group]
                group_df = engagemet[engagemet['Award Reference'].isin(group_refs)]
                national_p_group[count] = [national_p_group[count], group_df]
                count += 1

            # renaming 
            for group in national_p_group:
                group[1]['Award Reference'] = group[0]
        
            fellows_df, sprintET_df, university_rt_df  = national_p_group[0][1], national_p_group[1][1], national_p_group[2][1]

            appl_fellows_df = fellows_df.groupby("Award Reference").agg({'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Patients, Cares, Patient Groups':['sum']})
            appl_sprintET_df = sprintET_df.groupby("Award Reference").agg({'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Patients, Cares, Patient Groups':['sum']})
            appl_university_rt_df = university_rt_df.groupby("Award Reference").agg({'Policymakers':['sum'], 'Professional Practitioners':['sum'],'General Public':['sum'], 'Patients, Cares, Patient Groups':['sum']})
            
            appl_fellows_df.columns = appl_fellows_df.columns.droplevel(1)
            appl_sprintET_df.columns = appl_sprintET_df.columns.droplevel(1)
            appl_university_rt_df.columns = appl_university_rt_df.columns.droplevel(1)
            
            # merging all DataFrames together
            merged_df = pd.concat([appl_fellows_df, appl_sprintET_df, appl_university_rt_df])
            merged_df['Award_Reference_1'] = merged_df.index
            merged_df = merged_df.reindex(['Award_Reference_1','Policymakers','Professional Practitioners', 'General Public', 'Patients, Cares, Patient Groups'], axis=1)

            # plot a Stacked Bar Chart using matplotlib 
            stacked_bar_plot_percentage(merged_df, "Award_Reference_1", plt_tilte, labels)

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

    Geographical Reach for National Priority
    engagement.geographical_reach_2019(rf_2019_wb, np_2019_award_refs_dict, 'Geographical Reach for National Priority')
    # Geographical Reach for Activities
    engagement.geographical_reach_2019(rf_2019_wb, act_2019_award_refs_dict, 'Geographical Reach for Activities Group')
    # Geographical Reach for Community Groups
    engagement.geographical_reach_2019(rf_2019_wb, comm_2019_award_refs_dict, 'Geographical Reach for Community Groups')

    # Other Audiences 
    engagement.other_audience_2019(rf_2019_wb, np_2019_award_refs_dict, ['Applied Analytics', 'Better Care', 'Human Phenome', 'Understanding Causes of Disease', 'Clinical Trials', 'Improving Public Health'])
    engagement.other_audience_2019(rf_2019_wb, act_2019_award_refs_dict, ['HDRUK central infrastructure activities', 'HDRUK central PPPEI activities', 'HDRUK central training activities'])
    engagement.other_community_audience_2019(rf_2019_wb, comm_2019_award_refs_dict, ['Fellows', 'Sprint Exemplar Teams', 'University Research Teams'])

    # Impact
    engagement.impact_of_hdruk_research(rf_2019_wb, np_2019_award_refs_dict, 'Impact of HDRUK National Priority', ['Applied Analytics', 'Better Care', 'Human Phenome', 'Understanding Causes of Disease', 'Clinical Trials', 'Improving Public Health'])
    engagement.impact_of_hdruk_research(rf_2019_wb, act_2019_award_refs_dict, 'Impact of HDRUK Activities Group', ['HDRUK central infrastructure activities', 'HDRUK central PPPEI activities', 'HDRUK central training activities'])
    engagement.impact_of_community_audience_2019(rf_2019_wb, comm_2019_award_refs_dict, 'Impact of HDRUK Community Group', ['Central Infrastructure Activities', 'Central PPPEI Activities', 'Central Training Activities'])

if '__main__' == __name__:
    main()
