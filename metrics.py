from hdruk_groups import *
import plotly.express as px
import plotly


PATH_TO_NP_AWARD_REFS = 'hdruk_groups/national_priority_group_award_refs.json'


def read_json(path_to_json):
    
    with open(path_to_json) as fp:
        data_dict = json.load(fp)

    return data_dict


def get_international_collaborations(workbook, award_refs_dict):
    
    collaborations_df = workbook['Collaborations']

    collaborations_filtered_df = pd.DataFrame(columns = collaborations_df.columns)

    for key in award_refs_dict:
        value = award_refs_dict[key][0]        
        collaborations_filtered_df = collaborations_filtered_df.append(
            collaborations_df.loc[collaborations_df['Award Reference'] == value])

    np_country_counts = collaborations_filtered_df['Country'].value_counts().to_dict()

    for key in np_country_counts:
        np_country_counts[key] = [np_country_counts[key]]

    gapminder = px.data.gapminder().query("year == 2007")

    np_country_counts_df = pd.DataFrame(np_country_counts).T.reset_index()
    np_country_counts_df.columns=['country', 'count']

    df=pd.merge(gapminder, np_country_counts_df, how='left', on='country')

    fig = px.choropleth(df, locations="iso_alpha",
                        color="count", 
                        hover_name="country", # adding hover information
                        color_continuous_scale=px.colors.sequential.Plasma)

    
    plotly.offline.plot(fig, filename='outputs/national_priority_international_colabs.html')


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

    np_award_refs_dict = read_json(PATH_TO_NP_AWARD_REFS)
    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)

    # Getting national priority international collaborations
    get_international_collaborations(rf_2019_wb, np_award_refs_dict)

    # Getting national priority UK-wide collaborations
    np_uk_region_counts_dict = uk_collaborations.get_region_counts(rf_2019_wb)
    np_uk_region_counts_df = uk_collaborations.add_region_area_codes(np_uk_region_counts_dict)
    np_uk_region_counts_df.to_csv('outputs/np_uk_region_colab_counts.csv', index=False)



if '__main__' == __name__:
    main()