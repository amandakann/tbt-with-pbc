library(ggplot2)
library(tidyverse)
library(stringr)

# Change this variable to plot a different URIEL feature
feature <- "S_ADJECTIVE_AFTER_NOUN"

file <- read.csv(file.path(dirname(rstudioapi::getSourceEditorContext()$path), "output", "db_intralang.csv"))
df <- data.frame(file$mean, file$sdev, file$feature, file$combined_class)
labels <- c("dephead" = "Dependent-head", "headdep" = "Head-dependent", "both" = "Both orders possible", "other" = "No data / disagreement")

df <- df %>% filter(file.feature==feature) %>% group_by(file.combined_class)
df$file.combined_class <- recode(df$file.combined_class, !!! labels)
  
df <- df %>%mutate(label = paste0(file.combined_class, ' (n = ', n(), ')'))

figure <- ggplot(df, aes(x=file.feature, y=file.sdev, group=label, fill=str_wrap(label, width=22))) + 
  geom_boxplot(outlier.size=3, alpha = 0.7) +
  xlab("") + ylab("Standard deviation of inter-doculect variation") + 
  theme_minimal() +
  labs(title=paste0("Inter-doculect variation \nfor adjective/noun order"),fill=str_wrap('Classification in typological databases', width = 22)) +
  theme(plot.title=element_text(hjust=0.5, size=20), axis.text=element_text(size=11), axis.title = element_text(size=16), axis.title.x=element_blank(), axis.text.x=element_blank(),
        legend.title=element_text(size=14, face = "bold", hjust=0.5), legend.text=element_text(size=12)) +
  scale_fill_manual(values = c("#117733","#DDCC77","#AA4499","#BBBBBB"))

ggsave(file.path(dirname(rstudioapi::getSourceEditorContext()$path), "output", "figures", "figure1.pdf"), plot = figure, width = 8, height = 6)
