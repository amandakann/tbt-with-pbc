import os
from tabulate import tabulate
import pandas as pd

def main():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'db_intralang.csv'), index_col=0)
    summary = df[["feature", "sdev"]].groupby("feature").describe()["sdev"]
    print(tabulate(summary.round(decimals=3)[['count', 'mean', 'std']], tablefmt="latex"))

if __name__ == "__main__": main()