library(ggplot2)
library(scales)
library(tidyverse)
library(knitr)
library(psych)
library(corrplot)
library(janitor)
library(broom)
library(rstatix) 
library(patchwork)
library(kableExtra)
library(chisq.posthoc.test)
library(datarium) 
library(rstatix) 

ultra_rankings<-read.csv("ultra_rankings.csv") %>% 
  mutate(runner=str_to_title(runner), finished_race=ifelse(is.na(rank),"DidNotFinish", "Finished"))


race<-read.csv("race.csv") %>% 
  mutate(participation=str_to_title(participation), date= as.character(date)) 

merged_data<-ultra_rankings %>% 
  inner_join(race, by= "race_year_id") %>% 
  filter(age> 0,distance>0,time_in_seconds >0) 


ultra_rankings_2 <- ultra_rankings %>% 
  mutate(runner = str_to_title(runner), 
         finished_race=ifelse(is.na(rank),"DidNotFinish", "Finished"), 
         age_range=case_when( age<=30 ~ "<30", age>30 & age<=40 ~ "30-40", 
                              age>40 & age<=50 ~ "40-50", age>50 & age<=60 ~ "50-60", 
                              age>60 ~ "60+")) %>% filter(age> 10& age<= 90) 

full_data <- left_join(ultra_rankings_2,race, by= "race_year_id")

full_data <- full_data %>%
  mutate(distance_range = ifelse(distance < 150, "Less 150km", 
                                 ifelse( distance >= 150 & distance < 160,
                                         "150-160Km", ifelse( distance >= 160 & distance < 170, "160-170Km", "170-180Km"))), 
         gender = ifelse(gender=="W", "Women", ifelse(gender=="M", "Men", NA)) ) %>%
  filter(finished_race == "Finished") 

full_data_160_170 <- full_data %>%
  filter(distance_range=="160-170Km", 
         !is.na(gender) ) custom_colors_gender = c("Men" = "#669BBC", "Women" = "#E56B6F", "NA" = "#8D99AE") 

ggplot(full_data, aes(x = distance_range, y= time_in_seconds, fill = gender)) +
  geom_boxplot() + labs(x = "Distance", y = "Time in Seconds") + 
  scale_fill_manual(values = custom_colors_gender) + theme_minimal() 


age_contigency_table <- table( ultra_rankings_2$age_range, 
                               ultra_rankings_2$finished_race) 


kable(age_contigency_table, format = "latex", booktabs = TRUE) %>%
  kable_styling(position = "center") 

row_total <- rowSums(age_contigency_table) 
col_total <- colSums(age_contigency_table) 
total <- sum(age_contigency_table) 
expected <- outer(row_total, col_total, "*") / total kable(expected, format = "latex", booktabs = TRUE) %>%
  kable_styling(position = "center") 


chisq_results <- chisq.test(x = age_contigency_table) 

chisq_df <- data.frame(Statistic = chisq_results$statistic, p_value = chisq_results$p.value, df = chisq_results$parameter ) 

kable(chisq_df, format = "latex", booktabs = TRUE) %>%
  kable_styling(position = "center") 


posthoc_results <- chisq.posthoc.test(age_contigency_table) kable(posthoc_results, format = "latex", booktabs = TRUE) %>%
  kable_styling(position = "center") 


gender.grouping <- group_by(full_data_160_170, gender) 

outliers <- identify_outliers(gender.grouping, time_in_seconds) 
outliers <- outliers %>% filter(is.extreme == TRUE) # only women have extreme 

outliers full_data_160_170_2 <- full_data_160_170 %>%
  anti_join(outliers, by = c("runner", "time_in_seconds")) #shapiro_test(gender.grouping, time_in_seconds) 

test <- full_data_160_170_2 %>% 
  select(gender, time_in_seconds) %>%
  group_by(gender) %>% 
  summarise(n = n(), mean = mean(time_in_seconds, na.rm = TRUE), 
            sd = sd(time_in_seconds, na.rm = TRUE),, na = sum(is.na(time_in_seconds)) )

kable(test, format = "latex", booktabs = TRUE, align = "c") %>%
  kable_styling(latex_options = c("scale_down")) 

bin_width_fd <- 2 * IQR(full_data_160_170_2$time_in_seconds) / length(full_data_160_170_2$time_in_seconds)^(1/3) 

bin_width_scott <- 3.49 * sd(full_data_160_170_2$time_in_seconds) / length(full_data_160_170_2$time_in_seconds)^(1/3) 

gg_boxplot <- full_data_160_170_2 %>% 
  select(runner, distance_range, time_in_seconds, gender) %>%
  ggplot(aes(x = time_in_seconds, y = gender, fill = gender)) + geom_boxplot(staplewidth = 0.4) +
  scale_fill_manual(values = c("Men" = "#669BBC", "Women" = "#E56B6F")) + 
  labs(x = "Time in Seconds", y = "Gender") + theme(legend.position = "none") 

gg_qq<- full_data_160_170_2 %>% 
  select(runner, distance_range, time_in_seconds, gender) %>% 
  ggplot(aes(sample = time_in_seconds)) + geom_qq() + geom_qq_line() + facet_wrap(~gender) 

gg_hist <- full_data_160_170_2 %>% 
  select(runner, distance_range, time_in_seconds, gender) %>% 
  ggplot(aes(x = time_in_seconds)) + geom_histogram(colour = "white") + 
  labs(x = "Time in Seconds", y = "Count") + 
  scale_x_continuous( labels = label_number(scale_cut = cut_short_scale())) + 
  facet_wrap(~gender) (gg_boxplot / (gg_qq+gg_hist)) + 
  plot_layout(heights = c(3, 5)) 


t_results <- full_data_160_170_2 %>% 
  t_test(time_in_seconds ~ gender, alternative = "two.sided", var.equal = FALSE)


kable(t_results, format = "latex", booktabs = TRUE, align = "c") 

merged_data <- merged_data %>%
  filter(!is.na(distance), !is.na(time_in_seconds)) 

# Assumptions oulier inspection: 
dist_boxplot <- merged_data %>% ggplot(aes(x = distance)) +
  geom_boxplot(staplewidth = 0.4, width = 1) + ylim(-0.75, 0.75) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank()) 


time_boxplot <- merged_data %>% 
  ggplot(aes(x = time_in_seconds)) +
  geom_boxplot(staplewidth = 0.4, width = 1) + ylim(-0.75, 0.75) + 
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank()) 


# Assumptions normality inspection: Histogram and QQ-Plot 

dist_hist <- ggplot(merged_data, aes(x = distance)) + 
  geom_histogram(binwidth = 10, fill = "lightgreen", color = "black") + 
  labs(title = "Histogram of Distance Run", x = "Distance", y = "Frequency") 

time_hist <-ggplot(merged_data, aes(x = time_in_seconds)) + 
  geom_histogram(binwidth = 100, fill = "green", color = "black") + 
  labs(title = "Histogram of Time in Seconds", x = "Time in Seconds", y = "Frequency") 

dist_qqplot <- ggplot(merged_data, aes(sample = distance)) + 
  stat_qq() + stat_qq_line() + labs(title ="Q-Q Plot of Distance Run", 
                                    y = "Sample Quantiles", x = "Theoretical Quantiles") 

time_qqplot <- ggplot(merged_data, aes(sample = time_in_seconds)) + stat_qq() + 
  stat_qq_line() + labs(title = "Q-Q Plot of Time in Seconds", 
                        y = "Sample Quantiles", x = "Theoretical Quantiles") 

# Results at-a-glance 

combined_plot <- (dist_boxplot + time_boxplot) /
  (dist_hist + time_hist) / (dist_qqplot + time_qqplot) +
  plot_layout(heights = c(1, 1, 1)) combined_plot library(viridis) 

# For color scaling 

# EDA equivalent 

result correlation_original <- corr.test(merged_data$distance, merged_data$time_in_seconds, use = "complete.obs") 

# Calculate Spearman's rho 

correlation_spearman <- corr.test(merged_data$distance, merged_data$time_in_seconds, method = "spearman", use = "complete.obs") 
ggplot(merged_data, aes(x = distance, y = time_in_seconds)) + geom_bin2d(bins = 100) + # Density-based binning 
  scale_fill_viridis_c() + # Better color 
  scaling geom_smooth(method = "lm", col = "blue") + # Linear trend line 
  ggtitle(paste("Spearman's Correlation (rho): ", round(correlation_spearman$r, 3))) + xlab("Distance Ran") + ylab("Time in Seconds") + theme_minimal()






















