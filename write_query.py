from hdruk_groups import *

PATH_TO_DIMENSIONS_2018_EXPORT = "dimensions/Dimensions_2018.xlsx"
PATH_TO_DIMENSIONS_2019_EXPORT = "dimensions/ALL_Dimensions-Publication-2021-03-04_11-51-46.xlsx"

def write_doi_query(workbook, year):

    publications_df = workbook['Publications']

    doi_column = publications_df['DOI'].dropna()
    
    doi_unique = doi_column.drop_duplicates()

    OR_query_doi = ''
    count=0
    for doi in doi_unique:
        if count == 0:
            OR_query_doi = OR_query_doi + doi
        else:
            OR_query_doi = OR_query_doi + ' OR ' + doi
        count+=1

    doi_file = open("dimensions/doi_query_{}.txt".format(year), "wt")
    write_dois = doi_file.write(OR_query_doi)
    doi_file.close()


def write_publication_id_query(workbook, year):

    dimensions_df = workbook['Sheet1']

    pub_id_column = dimensions_df['Publication ID'].dropna()

    pub_id_unique = pub_id_column.drop_duplicates()

    OR_query_pub_id = 'id: ("'
    count=0
    for i in pub_id_unique:
        if count == 0:
            OR_query_pub_id = OR_query_pub_id + i
        else:
            OR_query_pub_id = OR_query_pub_id + '" OR "' + i
        count+=1

    OR_query_pub_id = OR_query_pub_id + '")'

    pub_id_file = open("dimensions/pub_id_query_{}.txt".format(year), "wt")
    write_ids = pub_id_file.write(OR_query_pub_id)
    pub_id_file.close()


def main():

    rf_2018_wb = read_workbook(PATH_TO_RESEARCHFISH_2018_DATA)
    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)

    dimensions_2018_export = read_workbook(PATH_TO_DIMENSIONS_2018_EXPORT)
    dimensions_2019_export = read_workbook(PATH_TO_DIMENSIONS_2019_EXPORT)


    write_doi_query(rf_2018_wb, "2018")
    write_doi_query(rf_2019_wb, "2019")
    write_publication_id_query(dimensions_2018_export, "2018")
    write_publication_id_query(dimensions_2019_export, "2019")

    


if '__main__' == __name__:
    main()