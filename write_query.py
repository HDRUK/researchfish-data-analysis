from hdruk_groups import *

def write_query(workbook):

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

    doi_file = open("dimensions/doi_query.txt", "wt")
    write_dois = doi_file.write(OR_query_doi)
    doi_file.close()


def main():

    rf_2018_wb = read_workbook(PATH_TO_RESEARCHFISH_2018_DATA)
    rf_2019_wb = read_workbook(PATH_TO_RESEARCHFISH_2019_DATA)

    write_query(rf_2019_wb)


if '__main__' == __name__:
    main()