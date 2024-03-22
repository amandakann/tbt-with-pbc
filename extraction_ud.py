import csv, os
from glob import glob
from operator import add
import xml.etree.ElementTree as ET
from grewpy import Corpus, Request

def count_headdep(filename:str, gov_upos:list[str], dep_upos:list[str], rel:str) -> list[int, int]:
    ud = Corpus(filename)

    dephead = ud.count(Request(f"GOV [upos={'|'.join(gov_upos)}]; DEP [upos={'|'.join(dep_upos)}]; GOV >> DEP; GOV -[{rel}]-> DEP"))
    headdep = ud.count(Request(f"GOV [upos={'|'.join(gov_upos)}]; DEP [upos={'|'.join(dep_upos)}]; GOV << DEP; GOV -[{rel}]-> DEP"))

    return(dephead, headdep)

def main(dirpath, label):
    values = []
    dirc = 0
    print(f"Total directories: {len(glob(f'{dirpath}/*'))}")
    for dirname in glob(f'{dirpath}/*'):
        dirc += 1
        if dirc % 10 == 0:
            print(f"Counting for {dirname.split('/')[-1]} ({dirc})")
        tree = ET.parse(f"{dirname}/stats.xml")
        root = tree.getroot()
        
        c = [0,0]
        iso, treebank = "", ""
        for filename in glob(f"{dirname}/*.conllu"):
            if iso == "":
                iso, treebank = filename.split('/')[-1].split('-')[0].split('_')
            c = list(map(add, c, count_headdep(filename, *labeldict[label])))
#        print(f"{iso}   {treebank} {root[0][0][0].text}  {c[0]} {c[1]}")
        values.append([iso, treebank, root[0][0][0].text, c[0], c[1]])
    with open(os.path.join(os.path.dirname(__file__), 'ud-parsed', f'ud_{label}.csv'), 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['iso','treebank','total_sentences','dep-head','head-dep'])
        writer.writerows(sorted(values))

if __name__ == "__main__":
#    main("resources/ud_sample")
    dirpath = os.path.join(os.path.dirname(__file__), 'data', 'ud-treebanks')
    labeldict = {
        "adp": [["NOUN", "PROPN"], ["ADP"], "case"],
        "adj": [["NOUN", "PROPN"], ["ADJ"], "amod"],
        "num": [["NOUN", "PROPN"], ["NUM"], "nummod"],
        "rel": [["NOUN", "PROPN"], ["VERB"], "acl"],
        "sub": [["VERB"], ["NOUN", "PROPN"], "nsubj"],
        "obl": [["VERB"], ["NOUN", "PROPN"], "obl"],
        "obj": [["VERB"], ["NOUN", "PROPN"], "obj"],
    }
    for label in labeldict.keys():
        main(dirpath, label)