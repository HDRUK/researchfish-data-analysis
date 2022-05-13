import csv
import json
import crossref_commons.retrieval
from pprint import pprint
import random

# https://api.crossref.org/works/10.1016/s0140-6736(21)01609-3

# https://observablehq.com/@d3/temporal-force-directed-graph
# https://observablehq.com/@d3/force-directed-graph
# https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8

def read_csv(filename):
    ROWS = []
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ROWS.append(row)
    return ROWS

def write_csv(data, filename, header, mode='w'):
    with open(filename, mode) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if mode == 'w': writer.writeheader()
        writer.writerows(data)

def crossref_loookup(doi):
    doi = doi.lower()
    META = {}
    try:
        ret = crossref_commons.retrieval.get_publication_as_json(doi)
    except ValueError as err:
        print(doi, err)
        META['Error'] = str(repr(err))
        return True, META
    data = ret
    try:
        if doi == data['DOI']:
            META['DOI'] = data['DOI']
            META['Publication'] = "".join(data['title'])
            META['Year'] = data['created']['date-parts'][0][0]
            META['Month'] = data['created']['date-parts'][0][1]
            META['Date'] = data['created']['date-parts'][0][2]
            for a in data['author']:
                if a.get('name', None) is not None:
                    author = a.get('name')
                else:
                    if a.get('given', None) is not None:
                        given = " ".join([s[0] for s in a['given'].split()][0])
                    else:
                        given = ""
                    author = " ".join([a['family'], given])
                if a['sequence'] == 'first':
                    META['Author'] = author    
                else:
                    META.setdefault('Co-Authors', [])
                    META['Co-Authors'].append(author)
    except KeyError as err:
        print(doi, err)
        META['Error'] = str(repr(err))
        return True, META
    return False, META
                


def get_missing_info(pubs):
    for i, p in enumerate(pubs):
        # doi = p.get('DOI', p.get('Publication'))
        doi = p['DOI']
        print("Processing: {}/{} {}".format(i,len(pubs), doi))
        # if p['\ufeffAuthor'] == "" or p['Co-Authors'] == "":
        if doi.startswith('10.'):
            err, meta = crossref_loookup(doi)
            if err:
                write_csv([p], 'pubs/errors.csv', ['DOI', 'Error'], 'a')
            else:
                p.update(meta)
                if p.get('Date', None) is None:
                    p['Date'] = str(random.randint(1,25))
                if p.get('Month', None) is None:
                    p['Month'] = str(random.randint(1,12))
                if p.get('Year', None) is None:
                    p['Year'] = str(random.randint(2018,2021))
    return pubs

def main():
    pubs = read_csv('pubs/doi.new.csv')
    print("Pubs:", pubs[0], len(pubs))

    pubs = get_missing_info(pubs)
    print(len(pubs))
    write_csv(pubs, 'pubs/pubs-fixed.new.csv', ['Author', 'Co-Authors', 'Publication', 'Date', 'Month', 'Year', 'DOI'])

if __name__ == '__main__':
    main()
    # doi = "10.1016/B978-0-12-812293-8.00017-7"
    # # ret = crossref_commons.retrieval.get_publication_as_json(doi)
    # error, meta = crossref_loookup(doi)
    # pprint(meta)
    # pprint(error)