# Code to calculate max sample sizes for UD langs (for Bern workshop abstract 2025)

# read filepath to df
df <- read.csv(paste0("/Users/amanda/git/tbt-with-pbc/ud-parsed", "/ud_obj.csv"))

# group by iso and make new sum column of dep-head and head-dep
df <- df %>%
  group_by(iso) %>%
  summarise(dep_head = sum(dep_head), head_dep = sum(head_dep))

#look at first 5 rows of df
head(df)
