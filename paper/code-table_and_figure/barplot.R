library(ggplot2)
library(scales)

data = read.table('overlap_counts.txt', sep = ' ', header = TRUE, row.names = NULL)

# data = data = read.table('overlap_counts_old.txt', sep = ' ', header = TRUE, row.names = NULL)

# data$size=factor(data$size) 

data$type = factor(data$type, levels = c('structure', 'activity', 'topic', 'interaction'))
data$count = factor(data$count)

# ggplot(data, aes(count, fill = type)) + geom_bar(position="dodge") + xlab('Size of Overlap') + ylab('Number of Users') #+ scale_y_continuous(trans=log10_trans())
ggplot(data, aes(type, fill = type)) + geom_bar() + facet_wrap(~ count, scales = 'free') + xlab('Number of Memberships') + ylab('Number of Users') + theme(text = element_text(size=20)) + theme(axis.text.x=element_text(angle=90))
ggsave('overlap_by_type.pdf')
