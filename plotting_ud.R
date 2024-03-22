library(ggplot2)
library(tidyverse)
library(ggpubr)
library(ggtext)
library(grid)

fig_plot <- function(filename){
  file <- read.csv(filename)
  df <- data.frame(file$ostling_head.dep_ratio, file$ud_head.dep_ratio, file$combined_class)
  labels <- c("dephead" = "Dependent-head", "headdep" = "Head-dependent", "both" = "Both orders possible", "other" = "No data / disagreement")
  df = df %>% group_by(file$combined_class)
  df$file.combined_class <- recode(df$file.combined_class, !!! labels)
  p <- ggplot(df, aes(x=file.ostling_head.dep_ratio, y=file.ud_head.dep_ratio, color=file.combined_class, shape=file.combined_class)) +
      xlab("Bible head/dep proportion") + ylab("UD head/dep proportion") + labs(color=str_wrap('Classification in typological databases', width = 22)) +
      geom_point(alpha = 0.5, size = 4) +
      xlim(0,1) + ylim (0,1) +
      theme_minimal() +
      theme(axis.text=element_text(size=11), axis.title = element_text(size=0),
            legend.position = "right", legend.title=element_text(size=18, face = "bold", hjust = 0.5), legend.text=element_text(size=14)) + 
      scale_color_manual(name = str_wrap('Classification in typological databases', width = 22), 
                         values = c("Dependent-head" = "#DDCC77",
                                    "Head-dependent" = "#AA4499",
                                    "Both orders possible" = "#117733",
                                    "No data / disagreement" = "#BBBBBB")) + 
      scale_shape_manual(name = str_wrap('Classification in typological databases', width = 22), 
                         values = c("Dependent-head" = 15,
                                  "Head-dependent" = 17,
                                  "Both orders possible" = 18,
                                  "No data / disagreement" = 20))
  return(p)
} 

chop <- function(path){
  id <- substr(basename(path), 3, 5)
  return(id)
}

hide_legend <- function(fig){
fig <- fig + theme(legend.position = "none")
  return(fig)
}

figures <- c()

files <- Filter(function(file) grepl("\\.csv$", file), list.files(file.path(dirname(rstudioapi::getSourceEditorContext()$path), "output", "ud-db"), full.names = TRUE))
labels <- lapply(files, FUN = chop)

figures <- lapply(files, FUN = fig_plot)
leg <- get_legend(figures[1])
leg <- as_ggplot(leg)
figures <- lapply(figures, FUN = hide_legend)
figures <- append(figures, list(leg))
plots <- ggarrange(plotlist = figures, ncol=4, nrow=2, labels = labels, vjust = 0.35, common.legend = FALSE) +
  theme(plot.margin = margin(0.5,0.5,0.5,0.5, "cm"))
plots2 <- annotate_figure(plots, left = textGrob("Ratio of head-dependent order in UD data", rot = 90, vjust = 1, gp = gpar(cex = 1.3)),
                bottom = textGrob("Ratio of head-dependent order in Bible data", gp = gpar(cex = 1.3)))
ggsave(file.path(dirname(rstudioapi::getSourceEditorContext()$path), "output", "figures", "figure2.pdf"), plot = plots2, width = 12, height = 6)

