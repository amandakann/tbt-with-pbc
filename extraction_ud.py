import csv, os
from glob import glob
from operator import add
import xml.etree.ElementTree as ET
import pyconll
import tqdm

def count_headdep(filename:str, gov_upos:list[str], dep_upos:list[str], rel:str) -> tuple[int, int]:
    ud = pyconll.load_from_file(filename)
    counts = {'dephead': 0, 'headdep': 0}
    for sentence in ud:
        for token in sentence:
            if token.upos in dep_upos and token.deprel == rel: 
                dep_idx = int(token.id)-1
                gov_idx = int(token.head)-1
                if sentence[gov_idx].upos in gov_upos:
                    if dep_idx < gov_idx:
                        counts['dephead'] += 1
                    else:
                        counts['headdep'] += 1

    return(counts['dephead'], counts['headdep'])

def extract_ud(data_dir, out_dir, label):
    values = []
    dirc = 0
    print(f"Total directories: {len(glob(f'{data_dir}/*'))}")
    for dirname in glob(f'{data_dir}/*'):
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
    with open(os.path.join(os.path.dirname(__file__), 'ud-parsed-test', f'ud_{label}.csv'), 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['iso','treebank','total_sentences','dep-head','head-dep'])
        writer.writerows(sorted(values))

def extract_conllu(data_dir, out_dir, dependencies):
    conllu_files = [f for f in os.listdir(data_dir) if f.endswith('.conllu') and os.path.isfile(os.path.join(data_dir, f))]
    if conllu_files:
        for conllu_file in tqdm(conllu_files, desc=f'Extracting from .conllu files in {os.path.basename(data_dir)}'):
            pass

def main(data_dir, is_ud, out_dir, dependencies):
    if is_ud:
        for label in dependencies:
            extract_ud(data_dir, out_dir, label)
    else:
        extract_conllu(data_dir, out_dir, dependencies)

    conllu_files = [f for f in os.listdir(data_dir) if f.endswith('.conllu') and os.path.isfile(os.path.join(data_dir, f))]
    if conllu_files:
        for conllu_file in tqdm(conllu_files, desc=f'Extracting from .conllu files in {os.path.basename(data_dir)}'):
            pass
    else:
        for subdir in tqdm([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))], desc=''):


if __name__ == "__main__":
#    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'ud-treebanks')
    data_dir = '/Users/amanda/data/ud2.12/ud-treebanks-v2.12'
    is_ud = True # Boolean flag to indicate whether file structure of data corresponds to UD releases
    out_dir = '/Users/amanda/data/ud2.12/ud-parsed-test'
    dependencies = {
        "adp": {"gov_upos": ["NOUN", "PROPN"], 
                "dep_upos": ["ADP"], 
                "rel": ["case"]},
        "adj": {"gov_upos": ["NOUN", "PROPN"], 
                "dep_upos": ["ADJ"], 
                "rel": ["amod"]},
        "num": {"gov_upos": ["NOUN", "PROPN"], 
                "dep_upos": ["NUM"], 
                "rel": ["nummod"]},
        "rel": {"gov_upos": ["NOUN", "PROPN"], 
                "dep_upos": ["VERB"], 
                "rel": ["acl"]},
        "sub": {"gov_upos": ["VERB"], 
                "dep_upos": ["NOUN", "PROPN"], 
                "rel": ["nsubj"]},
        "obl": {"gov_upos": ["VERB"], 
                "dep_upos": ["NOUN", "PROPN"], 
                "rel": ["obl"]},
        "obj": {"gov_upos": ["VERB"], 
                "dep_upos": ["NOUN", "PROPN"], 
                "rel": ["obj"]},
    }
    main(data_dir, is_ud, out_dir, dependencies)