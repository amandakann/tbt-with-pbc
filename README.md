# corpus-representativity
Code for comparing syntactic properties of texts extracted from parallel corpora to other same-language texts and typological databases.

This repository contains all code used to produce and visualize the results from the short paper *Massively Multilingual Token-Based Typology Using the Parallel Bible Corpus* (Kann, forthcoming) presented at LREC 2024. 
Please see the paper for further details.

## Dependencies
The following external libraries are required:

### Extracting syntactic properties from CoNLL-U corpora
- [grewpy](https://grew.fr/usage/python/)

Please follow the link above for installation instructions.

### Generating data tables
- [pandas](https://pypi.org/project/pandas/)
- [lang2vec](https://pypi.org/project/lang2vec/)
- [iso639-lang](https://pypi.org/project/iso639-lang/)

All libraries above are available on PyPI and can be installed using `pip`:
```
pip install package-name
```

### Producing the tables and figures in the paper (Kann, forthcoming)
- [tabulate](https://pypi.org/project/tabulate/) (Python)
- [ggplot2](https://cran.r-project.org/web/packages/ggplot2/index.html) and [stringr](https://cran.r-project.org/web/packages/stringr/index.html) from [tidyverse](https://cran.r-project.org/web/packages/tidyverse/) (R)
- [ggpubr](https://cran.r-project.org/web/packages/ggpubr/index.html) (R)

## Usage
### Extracting syntactic properties from CoNLL-U corpora
For convenience, the tables of syntactic properties extracted from [Universal Dependencies v2.12](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5150) and used in the paper (Kann, forthcoming) can be found pre-compiled in `/ud-parsed/`. If you only want to replicate the results of the paper, you can skip the steps in this section.

0. Install `grewpy` (see *#Dependencies*)
1. Download your desired dataset (eg the most recent release of [`ud-treebanks-vX.XX.tgz`](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5287)), and unpack it into `/data/ud-treebanks/`
2. Run `extraction_ud.py`:
    ```python3 extraction_ud.py```

### Generating data tables

0. Install the relevant dependencies (see *#Dependencies*)
1. Download the most recent release of the [Parallel text typology dataset](https://zenodo.org/doi/10.5281/zenodo.7506219) (Östling and Kurfalı, 2023), and unpack `word-order.json` into `/data/`
2. Download the most recent release of [Grambank](https://zenodo.org/doi/10.5281/zenodo.7740139), and unpack it into `/data/grambank/`
3. Run `data_tables.py` with one of two flags:
    - `-i` or `--intralang` to generate the inter-doculect data table (creates `/output/db_intralang.csv`)
    - `-u` or `--ud` to generate the three-way comparison data table (creates one csv file per syntactic feature in `/output/ud-db/`)
        - Optionally, add the flag `-t NN`, where NN is a non-negative integer, to set the lower threshold of occurrences per feature. If the sum of occurrences of a particular feature (including all possible orders) is below NN in a given corpus, it is excluded from the resulting data table. By default this value is 20, following [Levshina 2019](https://doi.org/10.1515/lingty-2019-0025).

### Producing the tables and figures in the paper (Kann, forthcoming)

For convenience, full-size versions of the figures in the paper can be found in `/output/figures/`.

0. Install the relevant dependencies (see *#Dependencies*)
1. Run `table_intralang.py` to generate the LaTeX code for Table 1.
2. Run `plotting_intralang.R` and `plotting_ud.R` in RStudio to generate Figure 1 and Figure 2, respectively.

## Output format
### Inter-doculect data table (`/output/db_intralang.csv`)
| Field | Header | Content | Example |
| --- | --- | --- | --- |
| 1 | (blank) | unique feature-language pair index | `345` |
| 2 | `feature` | URIEL label for syntactic feature | `S_NUMERAL_AFTER_NOUN` |
| 3 | `iso` | ISO 639-3 language identifier | `nya` |
| 4 | `count` | Number of doculects for language | `3` |
| 5 | `mean` | Mean of the `feature` order proportion in each doculect | `0.8963264659629592` |
| 6 | `sdev` | Standard deviation of the `feature` order proportion in each doculect | `0.06719308080192926` |
| 7 | `uriel_class` | Value of URIEL feature, if available | `headdep` |
| 8 | `gb_class` | Value of corresponding Grambank feature (combination), if available | `--` |
| 9 | `combined_class` | Combination of `uriel_class` and `gb_class` according to *#Matrix for deriving* | `headdep` |

### Three-way comparison data table (`/output/ud-db/S_[feature].csv`)
| Field | Header | Content | Example |
| --- | --- | --- | --- |
| 1 | `iso` | ISO 639-3 language identifier | `quc` |
| 2 | `language` | ISO 639-3 language name | `K'iche'` |
| 3 | `ud_occurrences` | Number of occurrences of `[feature]` in reference corpora | `118` |
| 4 | `ud_head-dep_ratio` | Proportion of occurrences of `[feature]` in reference corpora | `0.06779661016949153` |
| 5 | `ostling_head-dep_ratio` | Proportion of occurrences of `[feature]` in *Parallel text typology dataset* (Östling and Kurfalı, 2023) | `0.09677452602608458` |
| 6 | `diff` | Absolute difference between `ud_head-dep_ratio` and `ostling_head-dep_ratio` | `0.028977915856593053` |
| 7 | `uriel_class` | Value of URIEL feature, if available | `both` |
| 8 | `gb_class` | Value of corresponding Grambank feature (combination), if available | `dephead` |
| 9 | `combined_class` | Combination of `uriel_class` and `gb_class` according to *#Matrix for deriving* | `dephead` |

### Matrix for deriving `combined_class`

| | `headdep` | `dephead` | `both` | `--` | 
| --- | --- | --- | --- | --- |
| **`headdep`** | `headdep` | `other` | `headdep` | `headdep` |
| **`dephead`** | `other` | `dephead` | `dephead` | `dephead` |
| **`both`** | `headdep` | `dephead` | `both` | `both` |
| **`--`** | `headdep` | `dephead` | `both` | `other` |