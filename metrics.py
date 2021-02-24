from hdruk_groups import *
import plotly.express as px
import plotly

PATH_TO_RF_2018_AWARD_REFS = 'hdruk_groups/year_2018_group_award_refs.json'
PATH_TO_NP_2019_AWARD_REFS = 'hdruk_groups/national_priority_group_award_refs.json'
PATH_TO_COMM_2019_AWARD_REFS = 'hdruk_groups/community_group_award_refs.json'
PATH_TO_ACT_2019_AWARD_REFS = 'hdruk_groups/hdruk_activities_award_refs.json'


def read_json(path_to_json):
    
    with open(path_to_json) as fp:
        data_dict = json.load(fp)

    return data_dict


class international_collaborations(object):
    def collaborations_2018(workbook, award_refs_dict, filename_out):
        
        collaborations_df = workbook['Collaborations']

        collaborations_filtered_df = pd.DataFrame(columns = collaborations_df.columns)

        for key in award_refs_dict:
            for value in award_refs_dict[key]:
                collaborations_filtered_df = collaborations_filtered_df.append(
                    collaborations_df.loc[collaborations_df['File Reference'] == value])

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
        plotly.offline.plot(fig, filename='outputs/international_collabs/{}.html'.format(filename_out))

    def collaborations_2019(workbook, award_refs_dict, filename_out):
        
        '''
        PLOT FOR ENTIRE GROUP TYPE
        '''

        collaborations_df = workbook['Collaborations']

        collaborations_filtered_df = pd.DataFrame(columns = collaborations_df.columns)

        for key in award_refs_dict:
            for value in award_refs_dict[key]:       
                collaborations_filtered_df = collaborations_filtered_df.append(
                    collaborations_df.loc[collaborations_df['Award Reference'] == value])

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
        plotly.offline.plot(fig, filename='outputs/international_collabs/{}.html'.format(filename_out))


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

                plotly.offline.plot(fig, filename='outputs/international_collabs/{}_2019.html'.format(group[0]))


class uk_collaborations(object):
    def get_region_counts(workbook):

        collaborations_df = workbook['Collaborations']

        collaborations_UK_df = pd.DataFrame(columns = collaborations_df.columns)

        collaborations_UK_df = collaborations_UK_df.append(
            collaborations_df.loc[collaborations_df['Country'] == 'United Kingdom'])

        uk_region_counts_dict = collaborations_UK_df['Region'].value_counts().to_dict()

        return uk_region_counts_dict

    def add_region_area_codes(uk_region_counts_dict):

        uk_region_counts_df = pd.DataFrame.from_dict(uk_region_counts_dict, orient='index', columns=['Count'])
        uk_region_counts_df['Region'] = uk_region_counts_df.index
        uk_region_counts_df.reset_index(inplace=True, drop=True)

        uk_region_counts_df["Region"] = uk_region_counts_df["Region"].str.split(", ", n = 1, expand = True)

        # ONLY THE CODES FOR THE NPS 2019 DATA

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

        area_codes_list = [area_code[1] for area_code in area_codes_pairs_list]

        uk_region_counts_df.insert(loc=2, column='Area Code', value=area_codes_list)

        return uk_region_counts_df


def main():

    rfish_2018_award_refs_dict = read_json(PATH_TO_RF_2018_AWARD_REFS)
    np_2019_award_refs_dict = read_json(PATH_TO_NP_2019_AWARD_REFS)
    comm_2019_award_refs_dict = read_json(PATH_TO_COMM_2019_AWARD_REFS)
    act_2019_award_refs_dict = read_json(PATH_TO_ACT_2019_AWARD_REFS)

    rf_2018_wb = read_workbook(PATH_TO_RESEARCHFISH_2018_DATA)
    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)

    # Getting national priority international collaborations
    international_collaborations.collaborations_2018(rf_2018_wb, rfish_2018_award_refs_dict, 'researchfish_2018_international_colabs')
    international_collaborations.collaborations_2019(rf_2019_wb, np_2019_award_refs_dict, 'national_priority_2019_international_colabs')
    international_collaborations.collaborations_2019(rf_2019_wb, comm_2019_award_refs_dict, 'community_group_2019_international_colabs')
    international_collaborations.collaborations_2019(rf_2019_wb, act_2019_award_refs_dict, 'hdruk_activity_2019_international_colabs')

    # # Getting national priority UK-wide collaborations
    # np_2019_uk_region_counts_dict = uk_collaborations.get_region_counts(rf_2019_wb)
    # np_2019_uk_region_counts_df = uk_collaborations.add_region_area_codes(np_uk_region_counts_dict)
    # np_2019_uk_region_counts_df.to_csv('outputs/np_uk_region_colab_counts.csv', index=False)



if '__main__' == __name__:
    main()