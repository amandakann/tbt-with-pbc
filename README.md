# corpus-representativity
Code for comparing syntactic properties of texts extracted from parallel corpora to other same-language texts and typological databases.

This repository contains all code used to produce and visualize the results from the short paper *Massively Multilingual Token-Based Typology Using the Parallel Bible Corpus* (Kann, forthcoming) presented at LREC 2024. 
Please see the paper for further details.

## Dependencies
The following external libraries are required:

### Generating data tables
- [pandas](https://pypi.org/project/pandas/)
- [lang2vec](https://pypi.org/project/lang2vec/)
- [iso639-lang](https://pypi.org/project/iso639-lang/)

All libraries above are available on PyPI and can be installed using `pip`:
```
pip install package-name
```

### Extracting syntactic properties from CoNLL-U corpora
- [grewpy](https://grew.fr/usage/python/)

Please follow the link above for installation instructions.

### Producing the tables and figures in the paper (Kann, forthcoming)
- [tabulate](https://pypi.org/project/tabulate/) (Python)
- [ggplot2](https://cran.r-project.org/web/packages/ggplot2/index.html) and [stringr](https://cran.r-project.org/web/packages/stringr/index.html) from [tidyverse](https://cran.r-project.org/web/packages/tidyverse/) (R)
- [ggpubr](https://cran.r-project.org/web/packages/ggpubr/index.html) (R)

## Usage
### Extracting syntactic properties from CoNLL-U corpora
For convenience, the tables of syntactic properties extracted from [Universal Dependencies v2.12](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5150) and used in the paper (Kann, forthcoming) can be found pre-compiled in `/ud-parsed/`. If you want to replicate the results of the paper, you can skip the steps in this section.

0. Install `grewpy` (see #Dependencies)
1. Download your desired dataset (eg the most recent release of [`ud-treebanks-vX.XX.tgz`](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5287)), and unpack it into `/data/ud-treebanks/`
2. Run `extraction_ud.py`:
    ```python3 extraction_ud.py```

### Generating data tables

0. Install the relevant dependencies (see #Dependencies)
1. Download the most recent release of the [Parallel text typology dataset](https://zenodo.org/doi/10.5281/zenodo.7506219) (Östling and Kurfalı, 2023), and unpack `word-order.json` into `/data/`
2. Download the most recent release of [Grambank](https://zenodo.org/doi/10.5281/zenodo.7740139), and unpack it into `/data/grambank/`
3. Run `formatter_tool.py` with one of two flags:
    - `-i` or `--intralang` to generate the inter-doculect data table (creates `/output/db_intralang.csv`)
    - `-u` or `--ud` to generate the three-way comparison data table (creates one csv file per syntactic feature in `/output/ud-db/`)
        - Optionally, add the flag `-t NN`, where NN is a non-negative integer, to set the lower threshold of occurrences per feature. If the sum of occurrences of a particular feature (including all possible orders) is below NN in a given corpus, it is excluded from the resulting data table. By default this value is 20, following [Levshina 2019](https://doi.org/10.1515/lingty-2019-0025).

### Producing the tables and figures in the paper (Kann, forthcoming)

For convenience, full-size versions of the figures in the paper can be found in `/output/figures/`.

0. Install the relevant dependencies (see #Dependencies)
1. Run `table_intralang.py` to generate the LaTeX code for Table 1.
2. Run `plotting_intralang.R` and `plotting_ud.R` in RStudio to generate Figure 1 and Figure 2, respectively.