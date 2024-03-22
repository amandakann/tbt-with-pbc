import json, csv, os, statistics, glob, argparse
import pandas as pd
import lang2vec.lang2vec as l2v
from collections import defaultdict
from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue

fmap = {
    "adj":"S_ADJECTIVE_AFTER_NOUN",
    "adp":"S_ADPOSITION_AFTER_NOUN",
    "num":"S_NUMERAL_AFTER_NOUN",
    "obj":"S_OBJECT_AFTER_VERB",
    "obl":"S_OBLIQUE_AFTER_VERB",
    "rel":"S_RELATIVE_AFTER_NOUN",
    "sub":"S_SUBJECT_AFTER_VERB",
}

gbmap = {
        # maps feature name to list of sets representing conditions for dep-head [0] and head-dep [1] AND flexible order [2]
        "S_ADJECTIVE_AFTER_NOUN":[{"GB193-1"}, {"GB193-2"}, {"GB193-3"}],
        "S_ADPOSITION_AFTER_NOUN":[{"GB074-1", "GB075-0"}, {"GB075-1", "GB074-0"}, {"GB074-1", "GB075-1"}],
        "S_NUMERAL_AFTER_NOUN":[{"GB024-1"}, {"GB024-2"}, {"GB024-3"}],
        "S_RELATIVE_AFTER_NOUN":[{"GB328-1", "GB327-0"}, {"GB327-1", "GB328-0"}, {"GB327-1", "GB328-1"}],
    }

feature_names = ['S_SVO', 'S_SOV', 'S_VSO', 'S_VOS', 'S_OVS', 'S_OSV', 'S_SUBJECT_BEFORE_VERB', 'S_SUBJECT_AFTER_VERB', 'S_OBJECT_AFTER_VERB', 'S_OBJECT_BEFORE_VERB', 'S_SUBJECT_BEFORE_OBJECT', 'S_SUBJECT_AFTER_OBJECT', 'S_GENDER_MARK', 'S_SEX_MARK', 'S_DEFINITE_AFFIX', 'S_DEFINITE_WORD', 'S_INDEFINITE_AFFIX', 'S_INDEFINITE_WORD', 'S_POSSESSIVE_PREFIX', 'S_POSSESSIVE_SUFFIX', 'S_ADPOSITION_BEFORE_NOUN', 'S_ADPOSITION_AFTER_NOUN', 'S_POSSESSOR_BEFORE_NOUN', 'S_POSSESSOR_AFTER_NOUN', 'S_ADJECTIVE_BEFORE_NOUN', 'S_ADJECTIVE_AFTER_NOUN', 'S_DEMONSTRATIVE_WORD_BEFORE_NOUN', 'S_DEMONSTRATIVE_WORD_AFTER_NOUN', 'S_DEMONSTRATIVE_PREFIX', 'S_DEMONSTRATIVE_SUFFIX', 'S_NUMERAL_BEFORE_NOUN', 'S_NUMERAL_AFTER_NOUN', 'S_RELATIVE_BEFORE_NOUN', 'S_RELATIVE_AFTER_NOUN', 'S_RELATIVE_AROUND_NOUN', 'S_NOMINATIVE_VS_ACCUSATIVE_MARK', 'S_ERGATIVE_VS_ABSOLUTIVE_MARK', 'S_NEGATIVE_WORD_BEFORE_VERB', 'S_NEGATIVE_PREFIX', 'S_NEGATIVE_WORD_AFTER_VERB', 'S_NEGATIVE_SUFFIX', 'S_NEGATIVE_WORD_BEFORE_SUBJECT', 'S_NEGATIVE_WORD_AFTER_SUBJECT', 'S_NEGATIVE_WORD_BEFORE_OBJECT', 'S_NEGATIVE_WORD_AFTER_OBJECT', 'S_NEGATIVE_WORD_INITIAL', 'S_NEGATIVE_WORD_FINAL', 'S_NEGATIVE_WORD_ADJACENT_BEFORE_VERB', 'S_NEGATIVE_WORD_ADJACENT_AFTER_VERB', 'S_PLURAL_PREFIX', 'S_PLURAL_SUFFIX', 'S_PLURAL_WORD', 'S_OBJECT_HEADMARK', 'S_OBJECT_DEPMARK', 'S_POSSESSIVE_HEADMARK', 'S_POSSESSIVE_DEPMARK', 'S_TEND_HEADMARK', 'S_TEND_DEPMARK', 'S_TEND_PREFIX', 'S_TEND_SUFFIX', 'S_ANY_REDUP', 'S_CASE_PREFIX', 'S_CASE_SUFFIX', 'S_CASE_PROCLITIC', 'S_CASE_ENCLITIC', 'S_CASE_MARK', 'S_COMITATIVE_VS_INSTRUMENTAL_MARK', 'S_NUMCLASS_MARK', 'S_ADJECTIVE_WITHOUT_NOUN', 'S_PERFECTIVE_VS_IMPERFECTIVE_MARK', 'S_PAST_VS_PRESENT_MARK', 'S_FUTURE_AFFIX', 'S_TAM_PREFIX', 'S_TAM_SUFFIX', 'S_DEGREE_WORD_BEFORE_ADJECTIVE', 'S_DEGREE_WORD_AFTER_ADJECTIVE', 'S_POLARQ_MARK_INITIAL', 'S_POLARQ_MARK_FINAL', 'S_POLARQ_MARK_SECOND', 'S_POLARQ_WORD', 'S_POLARQ_AFFIX', 'S_SUBORDINATOR_WORD_BEFORE_CLAUSE', 'S_SUBORDINATOR_WORD_AFTER_CLAUSE', 'S_SUBORDINATOR_SUFFIX', 'S_PROSUBJECT_WORD', 'S_PROSUBJECT_AFFIX', 'S_PROSUBJECT_CLITIC', 'S_NEGATIVE_AFFIX', 'S_NEGATIVE_WORD', 'S_ANY_AGREEMENT_ON_ADJECTIVES', 'S_COMPLEMENTIZER_WORD_BEFORE_CLAUSE', 'S_COMPLEMENTIZER_WORD_AFTER_CLAUSE', 'S_VOX', 'S_XVO', 'S_XOV', 'S_OXV', 'S_OVX', 'S_OBLIQUE_AFTER_VERB', 'S_OBLIQUE_AFTER_OBJECT', 'S_OBLIQUE_BEFORE_VERB', 'S_OBLIQUE_BEFORE_OBJECT', 'S_ARTICLE_WORD_BEFORE_NOUN', 'S_ARTICLE_WORD_AFTER_NOUN']

def load_gb():
    with open(os.path.join(os.path.dirname(__file__), 'data', 'glottocode2iso.csv')) as ref:
        reader = csv.reader(ref)
        gc2iso = {k:v for k,v in reader}

    gb_data = defaultdict(set)
    missing = set()
    relevant_params = ["GB024", "GB074", "GB075", "GB193", "GB327", "GB328"]

    with open(os.path.join(os.path.dirname(__file__), 'data', 'grambank', 'values.csv')) as fin:
        gbreader = csv.reader(fin)
        next(gbreader)
        for line in gbreader:
            try:
                gb_iso = gc2iso[line[1]]
            except KeyError:
                missing.add(line[1])
                continue
            if line[2] in relevant_params:
                gb_data[gb_iso].add(line[4])
    
    print(f"--Grambank data loaded – {len(gb_data.keys())} languages; {(len(gb_data.keys())-len(missing))} present in glottocode2iso.csv")
#    print(gb_data["swe"])
    return(gb_data)

def uriel_checker(feature, iso):
    feature_index = feature_names.index(feature)
    opp_feature = feature.replace("AFTER", "BEFORE")
    opp_feature_index = feature_names.index(opp_feature)
    try:
        featureset = l2v.get_features(iso, l2v.fs_union("syntax_ethnologue","syntax_sswl","syntax_wals"))
        headdep = featureset[iso][feature_index]
        dephead = featureset[iso][opp_feature_index]
        if headdep == 0 and dephead == 1:
            return "dephead"
        elif headdep == 1 and dephead == 0:
            return "headdep"
        elif headdep == 1 and dephead == 1:
            return "both"
        else:
#            print(f'--Note: no relevant URIEL data for this feature for ({iso})')
            return "--"
    except Exception:
#        print(f'--Warning: no URIEL entry for ({iso})')
        return "--"

def grambank_checker(gb_data, feature, iso):
    if feature not in gbmap.keys():
        return '--'
    try:
        gb_tags = gb_data[iso]
    except KeyError:
#        print(f'--Warning: no GramBank data for ({iso})')
        return "--"
    if gbmap[feature][0].issubset(gb_tags):
        return "dephead"
    elif gbmap[feature][1].issubset(gb_tags):
        return "headdep"
    elif gbmap[feature][2].issubset(gb_tags):
        return "both"
    else:
#        print(f'--Note: no exclusive GB tag for ({iso})')
        return "--"
    
def combiner(uriel, gb):
    tags = {uriel, gb}
    if "dephead" in tags and "headdep" not in tags:
        return "dephead"
    elif "headdep" in tags and "dephead" not in tags:
        return "headdep"
    elif "both" in tags:
        return "both"
    else:
        return "other"

def intralang_formatter():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'word-order.json')
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'output')):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'output'))
    foutpath = os.path.join(os.path.dirname(__file__), 'output', 'db_intralang.csv')
    multiples = []
    gb_data = load_gb()
    with open(json_path) as f:
        projected = json.load(f)
    features = list(projected.keys())
    for feature in features:
        data = defaultdict(list)
        for k, v in projected[feature].items():
            k_iso = k[:3]
            data[k_iso].append(v)
        for k, v in data.items():
            if len(v) >= 2:
                uriel_value = uriel_checker(feature, k)
                grambank_value = grambank_checker(gb_data,feature,k)
                multiples.append([feature, k, len(v), statistics.mean(v), statistics.stdev(v), uriel_value, grambank_value, combiner(uriel_value,grambank_value)])
    df = pd.DataFrame(multiples, columns=["feature", "iso", "count", "mean", "sdev", "uriel_class", "gb_class", "combined_class"])
    df.to_csv(foutpath)
    print(f"Wrote data for {len(df.index)} languages to {foutpath}!")

def ud_formatter(csvfile, occurrence_threshold):
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'word-order.json')
    feature_ind = os.path.splitext(os.path.basename(csvfile))[0][-3:]
    feature = fmap[feature_ind]
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'output', 'ud-db')):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'output', 'ud-db'))
    foutpath = os.path.join(os.path.dirname(__file__), 'output', 'ud-db', f'{feature}.csv')
    gb_data = load_gb()
    projected_data = defaultdict(list)
    with open(json_path) as f:
        projected = json.load(f)
    for k, v in projected[feature].items():
        k_iso = k[:3]
        projected_data[k_iso].append(v)

    langs = defaultdict(lambda: [0,0])
    whichlangs = [[],[],[]]
    with open(csvfile) as fin:
        lines = csv.reader(fin, delimiter=',')
        next(lines)
        for line in lines:
            try: 
                lg = Lang(line[0])
            except InvalidLanguageValue as e:
                # print(e.msg)
                continue
            prep = int(line[3])
            postp = int(line[4])
            if prep+postp:
                langs[lg.pt3][0] += prep
                langs[lg.pt3][1] += postp
        dout=[]
        with open(foutpath, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow(['iso','language','ud_occurrences','ud_head-dep_ratio','ostling_head-dep_ratio','diff','uriel_class','gb_class','combined_class'])
            for k,v in sorted(langs.items()):
                if k in projected_data.keys() and sum(v) >= occurrence_threshold:
                    proj_ratio = statistics.mean(projected_data[k])
                    whichlangs[0].append(k)
                    uriel_value = uriel_checker(feature, k)
                    grambank_value = grambank_checker(gb_data,feature,k)
                    writer.writerow([k,Lang(k).name,sum(v),v[1]/sum(v),proj_ratio,abs((v[1]/sum(v))-proj_ratio),uriel_value,grambank_value,combiner(uriel_value,grambank_value)])
                    dout.append(abs((v[1]/sum(v))-proj_ratio))
                elif k in projected_data.keys() and sum(v) < occurrence_threshold:
                    whichlangs[1].append(k)
                elif k not in projected_data.keys():
                    whichlangs[2].append(k)
        print(f"Wrote data for {len(dout)} languages to {foutpath}!")
#        print(f"{feature} & {len(dout)} & {round(statistics.mean(dout), 3)} & {round(statistics.stdev(dout), 3)} \\\\")

def main():
    parser = argparse.ArgumentParser(description="This program formats data files for studying parallel corpus representativity.")
    parser.add_argument("-i", "--intralang", action="store_true", help="Run intralang_formatter")
    parser.add_argument("-u", "--ud", action="store_true", help="Run ud_formatter")
    parser.add_argument("-t", type=int, default=20, help="Specifies feature occurrence threshold for inclusion of UD corpus (default 20)")
    args = parser.parse_args()

    if args.intralang:
            intralang_formatter()
    elif args.ud:
        for filename in glob.glob(os.path.join(os.path.dirname(__file__), 'ud-parsed', '*.csv')):
            ud_formatter(filename, args.t)
    else:
        print("No valid option specified -- please use --intralang or --ud.")

if __name__ == "__main__": main()