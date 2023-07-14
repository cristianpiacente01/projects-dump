# PIACENTE CRISTIAN 866020 - PROBABILITA' E STATISTICA PER L'INFORMATICA, A.A 2021-22, UNIMIB

#install.packages("readxl")
#install.packages("ggpubr")
library("readxl") # read .xls
library("crayon") # colored output on console
library("ggpubr") # to use ggpaired

main <- function() {
  sales_data <- read_excel("vendite.xls") # imports the dataset into a dataframe
  
  before_color <- "lightblue" # color for Prima
  after_color <- "lightgreen" # color for Dopo
  
  # print descriptive statistics indexes
  cat(bold("Statistica descrittiva - indici\n")) 
  print_descr(sales_data$Prima, "Prima della campagna") 
  print_descr(sales_data$Dopo, "Dopo la campagna")
  
  # save to png graphs
  save_hist_and_norm(sales_data$Prima,
                     "Dati precedenti alla campagna pubblicitaria",
                     "Numero vendite",
                     "Numero punti vendita",
                     before_color, # bins color in the histogram
                     "blue", # normal curve color
                     "istogramma_prima.png")

  save_hist_and_norm(sales_data$Dopo,
                     "Dati successivi alla campagna pubblicitaria",
                     "Numero vendite",
                     "Numero punti vendita",
                     after_color,
                     "darkgreen",
                     "istogramma_dopo.png")
  
  save_two_boxplot(sales_data$Prima,
                   sales_data$Dopo,
                   "Confronto tra Boxplot, prima e dopo la campagna pubblicitaria",
                   c("Prima della campagna", "Dopo la campagna"),
                   "Numero vendite",
                   before_color,
                   after_color,
                   "boxplot_prima_e_dopo.png")
  
  save_paired(sales_data,
              "Prima",
              "Dopo",
              "Confronto prima e dopo la campagna pubblicitaria",
              "",
              "Numero vendite",
              before_color,
              after_color,
              "confronto_paired.png")
  
  
  # print to console paired T-test
  t_test_paired(sales_data$Dopo, sales_data$Prima)
  
}

t_test_paired <- function(first, second) {
  cat(blue$bold("[Paired T-Test, alpha = 0.05, mu_0 = 0, alternative = greater]"), "\n")
  diff_vec <- first - second
  n <- length(first)
  cat("n: ", bold$green(n), "\n")
  cat("Mean of the differences: ", bold$green(mean(diff_vec)), "\n")
  cat("Variance of the differences: ", bold$green(var(diff_vec)), "\n")
  cat("Standard deviation of the differences: ", bold$green(sd(diff_vec)), "\n")
  t <- mean(diff_vec) / sd(diff_vec) * sqrt(n)
  cat("t: ", bold$green(t), "\n")
  cat(sprintf("t-student df = %d, alpha = 0.05: ",n-1), bold$green(qt(0.95, n-1)), "\n")
  
  t.test(first, second, paired = TRUE, alternative = "greater")
  
}

print_descr <- function(data, name) {
  # Statistica descrittiva
  
  # Indici di posizione
  # Media campionaria: 
  # Primo quartile: 
  # Mediana campionaria: 
  # Terzo quartile: 
  
  # Indici di variabilità
  # Varianza campionaria: 
  # Deviazione standard campionaria: 
  # Scarto interquartile: 
  # Range: 
  
  
  cat("--- ", green$bold(name), " ---\n")
  cat(blue$bgBlack$bold("Indici di posizione\n"))
  cat(red("Media campionaria: "), white$bgBlack$bold(mean(data)), "\n")
  cat(red("Primo quartile: "), white$bgBlack$bold(quantile(data, 0.25, type = 2)), "\n") # type = 2 is the quantile we use
  cat(red("Mediana campionaria: "), white$bgBlack$bold(median(data)), "\n")
  cat(red("Terzo quartile: "), white$bgBlack$bold(quantile(data, 0.75, type = 2)), "\n")
  cat(blue$bgBlack$bold("\nIndici di variabilità\n"))
  cat(red("Varianza campionaria: "), white$bgBlack$bold(var(data)), "\n")
  cat(red("Deviazione standard campionaria: "), white$bgBlack$bold(sd(data)), "\n")
  cat(red("Scarto interquartile: "), white$bgBlack$bold(IQR(data, type = 2)), "\n")
  cat(red("Range: "), white$bgBlack$bold(range(data)), "\n\n")
  
}

save_paired <- function(data,
                        cond1,
                        cond2,
                        main_title,
                        x_title,
                        y_title,
                        first_color,
                        second_color,
                        filename) {
  
  ggpaired(data, 
           cond1 = cond1,
           cond2 = "Dopo",
           fill = "condition", 
           title = main_title,
           xlab = x_title,
           ylab = y_title,
           line.color = "gray",
           palette = c(first_color, second_color))
  
  ggsave(filename)
  
}
                        

save_two_boxplot <- function(first,
                             second,
                             main_title,
                             names,
                             y_title,
                             first_color,
                             second_color,
                             filename) {
  begin_png(filename)
  
  plot_two_boxplot(first, 
                   second, 
                   main_title, 
                   names, 
                   y_title, 
                   first_color,
                   second_color)
  
  
  end_png()
}

plot_two_boxplot <- function(first,
                             second,
                             main_title,
                             names,
                             y_title,
                             first_color,
                             second_color) {
  
  boxplot(first, 
          second, 
          col = c(first_color, second_color),
          names = names,
          main = main_title,
          ylab = y_title, 
          staplewex = 1) # long line for min and max
  # outliers are shown, I decided not to remove them
  
  # add labels
  
  text(y=boxplot.stats(first)$stats, 
       labels = boxplot.stats(first)$stats, 
       x = 0.51)
  
  text(y=boxplot.stats(second)$stats, 
       labels = boxplot.stats(second)$stats, 
       x = 2.48)
  
}

plot_hist <- function(data, main_title = "", x_title = "", y_title = "", color = "") {
  h <- hist(data, 
            main = main_title,
            xlab = x_title,
            ylab = y_title,
            axes = FALSE,
            col = color,
            plot = TRUE)
    
  show_axes(h)
  return(h)
}

save_hist_and_norm <- function(data, main_title, x_title, y_title, h_color, n_color, filename) {
  begin_png(filename)
  
  h <- plot_hist(data, main_title, x_title, y_title, h_color)
  
  # add normal curve
  curve(dnorm(x,
              mean = mean(data), 
              sd = sd(data))
            * diff(h$mids[1:2]) * length(data), 
              # from density to frequency: 
              # multiply by bin range and by the data vector length
        add = TRUE, 
        col = n_color, 
        lwd = 2)
  
  end_png()
}

show_axes <- function(histogram) {
  axis(1, at = histogram$breaks, labels = histogram$breaks) # show x axis
  axis(2, at = c(0, histogram$counts), labels = c(0, histogram$counts)) # show y axis
}

begin_png <- function(filename) {
  png(file = filename, 
      width = 900,
      height = 800) # pixels by default
}

end_png <- function() {
  dev.off() # close plotting device (png)
  invisible(NULL) # return nothing
}

main()



