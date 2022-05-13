import ast
import csv
import random


def read_csv(filename):
    ROWS = []
    with open(filename, 'r', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ROWS.append(row)
    return ROWS

def write_csv(data, filename, header):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def get_nodes(rows):
    ROWS = {}
    for i, r in enumerate(rows):
        print(r['DOI'])
        # co_authors = [ca.strip() for ca in r['Co-Authors'].split(',')]
        
        co_authors = ast.literal_eval(r['Co-Authors']) if r['Co-Authors'] != '' else []
        year = str(r.get('Year', str(random.randint(2018,2021))))
        month = str(r.get('Month', str("{:02d}".format(random.randint(1,12)))))
        date = str(r.get('Date', str("{:02d}".format(random.randint(1,27)))))
        author = r['Author'].strip()

        # print(
        #     r['DOI'],
        #     author,
        #     co_authors
        # )

        if author == "" and len(co_authors):
            author = co_authors[0]
            co_authors = co_authors[0] if len(co_authors) > 1 else []
        ROWS[i] = {
            "DOI": r['DOI'],
            "Author": author,
            "Co-Authors": co_authors,
            "Start Date": year + "-" + month + "-" + date
        }
    print("Collecting Entities...")
    ENTITIES = []
    for k, v in ROWS.items():
        ENTITIES.append(v['DOI'])
        ENTITIES.append(v['Author'])
        ENTITIES.extend(v['Co-Authors'])
    ENTITIES = list(set(ENTITIES))
    ENTITIES = sorted(ENTITIES)
    # ENTITIES = [{"Id": i,"Label": e} for i, e in enumerate(ENTITIES)]
    ALL_ENTITIES = {e:i for i, e in enumerate(ENTITIES)}
    

    print("Processing Nodes...")
    NODES = []
    # for i, e in enumerate(ENTITIES):
    for e, i in ALL_ENTITIES.items():
        if e.startswith('10.'):
            type = "publication"
        else:
            type = "author"
        NODES.append({
            "Id": i,
            "Label": e,
            "Type": type
        })
    
    print("Processing Edges...")
    EDGES = []
    id = 0
    for k, v in ROWS.items():
        EDGES.append({
            "Id": id,
            "Target": ALL_ENTITIES[v['DOI']],
            "Target Label": v['DOI'],
            "Source": ALL_ENTITIES[v['Author']],
            "Source Label": v['Author'],
            # "Source": [e['Id'] for e in ENTITIES if e['Label'] == v['DOI']][0],
            # "Target": [e['Id'] for e in ENTITIES if e['Label'] == v['Author']][0],
            "Start Date": v['Start Date'],
            "End Date": "2021-11-25",
            "Edge Type": "Author"
        })
        id += 1
        for ca in v['Co-Authors']:
            EDGES.append({
                "Id": id,
                "Target": ALL_ENTITIES[v['DOI']],
                "Target Label": v['DOI'],
                "Source": ALL_ENTITIES[ca],
                "Source Label": ca,
                # "Source": [e['Id'] for e in ENTITIES if e['Label'] == v['DOI']][0],
                # "Target": [e['Id'] for e in ENTITIES if e['Label'] == ca][0],
                "Start Date": v['Start Date'],
                "End Date": "2021-11-25",
                "Edge Type": "Author"
            })
            id += 1
    return ENTITIES, NODES, EDGES

def main():
    pubs = read_csv('data/pubs-fixed.csv')
    print("Pubs:", len(pubs))
    print(pubs[0])
    entities, nodes, edges = get_nodes(pubs)
    print("Nodes:", len(nodes), nodes[1])
    write_csv(nodes, 'graph/pub-nodes.csv', ['Id', 'Label', 'Type'])

    print("Edges:", len(edges), edges[1])
    write_csv(edges, 'graph/pub-edges.csv', ['Id', 'Source', 'Source Label', 'Target', 'Target Label', 'Edge Type','Start Date', 'End Date'])
    
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


if __name__ == '__main__':
    main()
    # check_encodings()
    