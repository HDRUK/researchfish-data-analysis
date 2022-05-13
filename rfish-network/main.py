import csv
from pprint import pprint

def read_csv(filename):
    ROWS = []
    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ROWS.append(row)
    return ROWS

def write_csv(data, filename, header):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def process_coauthors(data):
    for d in data:
        co_authors = [ca.replace(',', '').strip() for ca in d['Co-Authors'].split(';')]
        AUTHOR = ""
        COAUTHORS = []
        for ca in co_authors:
            ca_split = ca.split()
            if len(ca_split):
                if len(ca_split) > 1:
                    COAUTHORS.append(" ".join([ca_split[0], ca_split[1][0]]))
                else:
                    COAUTHORS.append(" ".join([ca_split[0]]))
                AUTHOR = COAUTHORS[0]
        d['Author'] = AUTHOR
        d['Co-Authors'] = COAUTHORS[1:]
    return data

def check_encodings():
    import pkgutil
    import encodings
    import os

    def all_encodings():
        modnames = set([modname for importer, modname, ispkg in pkgutil.walk_packages(
            path=[os.path.dirname(encodings.__file__)], prefix='')])
        aliases = set(encodings.aliases.aliases.values())
        return modnames.union(aliases)

    text = b'\x80'
    for enc in all_encodings():
        try:
            msg = text.decode(enc)
        except Exception:
            continue
        print('Decoding {t} with {enc} is {m}'.format(t=text, enc=enc, m=msg))

def main():
    data = read_csv('data/pubs.csv')
    data = process_coauthors(data)
    write_csv(data, 'data/pubs-fixed.csv', ['Author','Co-Authors', 'Publication', 'Date', 'Month','Year', 'DOI'])

if __name__ == '__main__':
    main()
    # check_encodings()
