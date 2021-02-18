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

    



def main():

    np_award_refs_dict = read_json(PATH_TO_NP_AWARD_REFS)
    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)
    get_international_collaborations(rf_2019_wb, np_award_refs_dict)

if '__main__' == __name__:
    main()
