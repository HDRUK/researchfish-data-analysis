from hdruk_groups import *
import plotly.express as px
import plotly
import matplotlib.pyplot as plt

PATH_TO_RF_2018_AWARD_REFS = 'hdruk_groups/year_2018_group_award_refs.json'
PATH_TO_NP_2019_AWARD_REFS = 'hdruk_groups/national_priority_group_award_refs.json'
PATH_TO_COMM_2019_AWARD_REFS = 'hdruk_groups/community_group_award_refs.json'
PATH_TO_ACT_2019_AWARD_REFS = 'hdruk_groups/hdruk_activities_award_refs.json'


def read_json(path_to_json):
    
    with open(path_to_json) as fp:
        data_dict = json.load(fp)

    return data_dict


def bar_plot(dataframe, x_label, y_lable, x_tick, filepath):
    ax = dataframe.plot.bar(figsize = (24, 10), width=0.8, rot = 6)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_lable)
    ax.set_xticklabels(x_tick)
    # plt.show()
    ax.figure.savefig(filepath)


def collaborations_impact(workbook, award_refs_dict, filepath1, filepath2):

    collaborations_df = workbook['Collaborations']

    subgroups_each_group = list(award_refs_dict.keys())

    count=0
    for key in award_refs_dict:
        group_refs = award_refs_dict[key]
        group_df = collaborations_df[collaborations_df['Award Reference'].isin(group_refs)]
                    
        subgroups_each_group[count] = [subgroups_each_group[count], group_df]

        subgroups_each_group[count][1]['Group'] = subgroups_each_group[count][0]

        count += 1

    list_dfs = [df[1] for df in subgroups_each_group]
    
    df_subgroups_impact = pd.concat(list_dfs)

    aggregated_subgroup_df = df_subgroups_impact.groupby('Group').agg({'Cultural Impact': ['sum'], 'Societal Impact': ['sum'], 'Economic Impact': ['sum'], 
    'Policy & Public Service Impact': ['sum'], 'No Impact Yet': ['sum']})

    combined_aggregated_subgroup_df = df_subgroups_impact[['Cultural Impact', 'Societal Impact', 'Economic Impact', 'Policy & Public Service Impact', 'No Impact Yet']]
    
    aggregated_subgroup_df.columns = aggregated_subgroup_df.columns.droplevel(1)
    aggregated_subgroup_df = aggregated_subgroup_df.T.reset_index()
    aggregated_subgroup_df = aggregated_subgroup_df.rename(columns={'index': 'Group'})

    agg_cols = aggregated_subgroup_df.columns.tolist()
    agg_cols.pop(0)

    # Change values to percentage
    aggregated_subgroup_df[agg_cols] = aggregated_subgroup_df[agg_cols].div(aggregated_subgroup_df[agg_cols].sum().sum(), axis=0).multiply(100)
    
    combined_aggregated_subgroup_df = combined_aggregated_subgroup_df.agg("sum", axis="rows")
    combined_agg_subgroup_df = combined_aggregated_subgroup_df.to_frame().reset_index()
    combined_agg_subgroup_df.columns = ['Group', 'National Priorities']

    # Change values to percentage
    combined_agg_subgroup_df[['National Priorities']] = combined_agg_subgroup_df[['National Priorities']].div(combined_agg_subgroup_df[['National Priorities']].sum().sum(), axis=0).multiply(100)

    bar_plot(aggregated_subgroup_df, "Impact Type", "Percentage", aggregated_subgroup_df['Group'], filepath1)
    bar_plot(combined_agg_subgroup_df, "Impact Type", "Percentage", aggregated_subgroup_df['Group'], filepath2)


class international_collaborations(object):
    def collaborations_2018(workbook, award_refs_dict, filename_out):
        
        collaborations_df = workbook['Collaborations']

        collaborations_filtered_df = pd.DataFrame(columns = collaborations_df.columns)

        for key in award_refs_dict:
            # for value in award_refs_dict[key]:
            #     collaborations_filtered_df = collaborations_filtered_df.append(
            #         collaborations_df.loc[collaborations_df['File Reference'] == value])
            group_refs = award_refs_dict[key]
            collaborations_filtered_df = collaborations_df[collaborations_df['File Reference'].isin(group_refs)]

        country_counts = collaborations_filtered_df['Country'].value_counts().to_dict()
        country_counts.pop('United Kingdom', None) # Remove United Kingdom from plot

        for key in country_counts:
            country_counts[key] = [country_counts[key]]

        gapminder = px.data.gapminder().query("year == 2007")

        country_counts_df = pd.DataFrame(country_counts).T.reset_index()
        country_counts_df.columns=['country', 'count']

        df=pd.merge(gapminder, country_counts_df, how='left', on='country')

        fig = px.choropleth(df, locations="iso_alpha",
                            color="count", 
                            hover_name="country", # adding hover information
                            color_continuous_scale=px.colors.sequential.Plasma)    
        
        # Plot for all award refs in HDR UK group
        plotly.offline.plot(fig, filename='outputs/collaborations/international_collabs/{}.html'.format(filename_out))

    def collaborations_2019(workbook, award_refs_dict, filename_out):
        
        '''
        PLOT FOR ENTIRE GROUP TYPE
        '''

        collaborations_df = workbook['Collaborations']

        collaborations_filtered_df = pd.DataFrame(columns = collaborations_df.columns)

        for key in award_refs_dict:
            # for value in award_refs_dict[key]:       
            #     collaborations_filtered_df = collaborations_filtered_df.append(
            #         collaborations_df.loc[collaborations_df['Award Reference'] == value])
            group_refs = award_refs_dict[key]
            collaborations_filtered_df = collaborations_df[collaborations_df['Award Reference'].isin(group_refs)]

        country_counts = collaborations_filtered_df['Country'].value_counts().to_dict()
        country_counts.pop('United Kingdom', None) # Remove United Kingdom from plot

        for key in country_counts:
            country_counts[key] = [country_counts[key]]

        gapminder = px.data.gapminder().query("year == 2007")

        country_counts_df = pd.DataFrame(country_counts).T.reset_index()
        country_counts_df.columns=['country', 'count']

        df=pd.merge(gapminder, country_counts_df, how='left', on='country')

        fig = px.choropleth(df, locations="iso_alpha",
                            color="count", 
                            hover_name="country", # adding hover information
                            color_continuous_scale=px.colors.sequential.Plasma)
        
        # Plot for all award refs in HDR UK group
        plotly.offline.plot(fig, filename='outputs/collaborations/international_collabs/{}.html'.format(filename_out))


        '''
        PLOT FOR SUBGROUPS IN GROUP TYPES
        '''
        country_counts_each_group = list(award_refs_dict.keys())

        count = 0
        for group in country_counts_each_group:
            group_refs = award_refs_dict[group]
            group_df = pd.DataFrame(columns = collaborations_df.columns)
            for ref in group_refs:
                group_df = group_df.append(collaborations_df.loc[collaborations_df['Award Reference'] == ref])
            
            country_counts_each_group[count] = [country_counts_each_group[count], group_df]

            count+=1

        for group in country_counts_each_group:

            group.append(group[1]['Country'].value_counts().to_dict())
            group[2].pop('United Kingdom', None) # Remove United Kingdom from plot

            if group[2] == {}:
                pass
            else:
                for key in group[2]:
                    group[2][key] = [group[2][key]]

                gapminder = px.data.gapminder().query("year == 2007")

                group_country_counts_df = pd.DataFrame(group[2]).T.reset_index()
                group_country_counts_df.columns=['country', 'count']

                group_df=pd.merge(gapminder, group_country_counts_df, how='left', on='country')

                fig = px.choropleth(group_df, locations="iso_alpha",
                                    color="count", 
                                    hover_name="country", # adding hover information
                                    color_continuous_scale=px.colors.sequential.Plasma)

                plotly.offline.plot(fig, filename='outputs/collaborations/international_collabs/{}_2019.html'.format(group[0]))


class uk_collaborations_2019(object):
    def get_region_counts(workbook, award_refs_dict):

        collaborations_df = workbook['Collaborations']

        collaborations_UK_df = pd.DataFrame(columns = collaborations_df.columns)

        collaborations_UK_df = collaborations_UK_df.append(
            collaborations_df.loc[collaborations_df['Country'] == 'United Kingdom'])

        # 2019 Groups
        uk_region_counts_each_group = list(award_refs_dict.keys())

        count = 0
        for group in uk_region_counts_each_group:
            group_refs = award_refs_dict[group]
            group_df = collaborations_UK_df[collaborations_UK_df['Award Reference'].isin(group_refs)]
            
            uk_region_counts_each_group[count] = [uk_region_counts_each_group[count], group_df]
            count += 1

        for i in uk_region_counts_each_group:
            i[1] = i[1]['Region'].value_counts().to_dict()

        return uk_region_counts_each_group

    def add_region_area_codes(uk_region_counts_each_group):

        area_codes_pairs_list = [
        ['Greater London','GLDN'], ['Cambridgeshire','CB'],
        ['Edinburgh','EH'], ['Oxfordshire','OX'],
        ['Borough of Stockport','SK'], ['City and County of Swansea','SA'],
        ['Nottingham','NG'], ['Manchester','M'],
        ['Northern Ireland','BT'], ['Bristol','BS'],
        ['Glasgow City','G'], ['City and Borough of Salford','M'],
        ['Cardiff','CF'], ['Rotherham','S'],
        ['City and Borough of Leeds','LS'], ['Slough','SL'],
        ['Aberdeen City','AB'], ['City of Leicester','LE'],
        ['Reading','RG'], ['City and Borough of Birmingham','B'],
        ['Liverpool','L'], ['Hampshire','SO'],
        ['Cheshire East','CH'], ['Dundee City','DD']
        ]

        areas_dict = {
            'Region': [area[0] for area in area_codes_pairs_list], 
            'Area Code': [area[1] for area in area_codes_pairs_list]}

        areas_df = pd.DataFrame(data=areas_dict)
        
        for i in uk_region_counts_each_group:
            if i[1] == {}:
                pass
            else:
                i[1] = pd.DataFrame.from_dict(i[1], orient='index', columns=['Count'])
                i[1]['Region'] = i[1].index
                i[1].reset_index(inplace=True, drop=True)
                i[1]["Region"] = i[1]["Region"].str.split(", ", n = 1, expand = True)
                i[1] = pd.merge(i[1], areas_df, on=["Region"])

        uk_region_counts_each_group = [group for group in uk_region_counts_each_group if len(group[1]) != 0]

        return uk_region_counts_each_group


def list_group_dataframe_pairs_to_csv(uk_region_counts_dfs, group_name):
    for group in uk_region_counts_dfs:
        group[1].to_csv('outputs/collaborations/uk_collabs/{}_uk_region_colab_counts.csv'.format(group[0]), index=False)

    col_headings = list(uk_region_counts_dfs[0][1].columns.values)

    count = 0
    for group in uk_region_counts_dfs:
        if count == 0:
            combined_df = group[1]
        else:
            combined_df = combined_df.append(group[1])
        count += 1

    combined_df = combined_df.groupby(["Region", "Area Code"])

    combined_df.sum().reset_index().to_csv('outputs/collaborations/uk_collabs/{}_uk_region_colab_counts.csv'.format(group_name), index=False)



def main():

    rfish_2018_award_refs_dict = read_json(PATH_TO_RF_2018_AWARD_REFS)
    np_2019_award_refs_dict = read_json(PATH_TO_NP_2019_AWARD_REFS)
    comm_2019_award_refs_dict = read_json(PATH_TO_COMM_2019_AWARD_REFS)
    act_2019_award_refs_dict = read_json(PATH_TO_ACT_2019_AWARD_REFS)

    rf_2018_wb = read_workbook(PATH_TO_RESEARCHFISH_2018_DATA)
    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)

    # Getting international collaborations
    international_collaborations.collaborations_2018(rf_2018_wb, rfish_2018_award_refs_dict, 'researchfish_2018_international_colabs')
    international_collaborations.collaborations_2019(rf_2019_wb, np_2019_award_refs_dict, 'national_priority_2019_international_colabs')
    international_collaborations.collaborations_2019(rf_2019_wb, comm_2019_award_refs_dict, 'community_group_2019_international_colabs')
    international_collaborations.collaborations_2019(rf_2019_wb, act_2019_award_refs_dict, 'hdruk_activity_2019_international_colabs')

    # Getting 2019 UK-wide collaborations
    np_2019_uk_region_counts_dict = uk_collaborations_2019.get_region_counts(rf_2019_wb, np_2019_award_refs_dict)
    np_2019_uk_region_counts_dfs = uk_collaborations_2019.add_region_area_codes(np_2019_uk_region_counts_dict)
    comm_2019_uk_region_counts_dict = uk_collaborations_2019.get_region_counts(rf_2019_wb, comm_2019_award_refs_dict)
    comm_2019_uk_region_counts_dfs = uk_collaborations_2019.add_region_area_codes(comm_2019_uk_region_counts_dict)
    act_2019_uk_region_counts_dict = uk_collaborations_2019.get_region_counts(rf_2019_wb, act_2019_award_refs_dict)
    act_2019_uk_region_counts_dfs = uk_collaborations_2019.add_region_area_codes(act_2019_uk_region_counts_dict)

    list_group_dataframe_pairs_to_csv(np_2019_uk_region_counts_dfs, 'National_Priorities')
    list_group_dataframe_pairs_to_csv(comm_2019_uk_region_counts_dfs, 'Community_Groups')
    list_group_dataframe_pairs_to_csv(act_2019_uk_region_counts_dfs, 'HDR_Activity_Groups')

    # Getting impact of collaborations
    collaborations_impact(rf_2019_wb, np_2019_award_refs_dict, 'outputs/collaborations/np_collaborations_impact.png',
    'outputs/collaborations/all_np_collaborations_impact.png')
    collaborations_impact(rf_2019_wb, comm_2019_award_refs_dict, 'outputs/collaborations/comm_collaborations_impact.png',
    'outputs/collaborations/all_comm_collaborations_impact.png')
    collaborations_impact(rf_2019_wb, act_2019_award_refs_dict, 'outputs/collaborations/hdr_act_collaborations_impact.png',
    'outputs/collaborations/all_hdr_act_collaborations_impact.png')


if '__main__' == __name__:
    main()