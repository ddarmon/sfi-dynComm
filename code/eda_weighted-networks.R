# weight.type = 'hashtag'
# weight.type = 'mention-retweet'
weight.type = 'transfer-entropy'; lag = 6

if (weight.type == 'hashtag'){
	data = read.csv('../data/content-full/twitter_network_hashtags_weighted.txt', sep = ' ', header = FALSE)

	weights = data$V3
} else if (weight.type == 'mention-retweet'){
	data = read.csv('../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt', sep = ' ', header = FALSE)

	weights = data$V3
} else if (weight.type == 'transfer-entropy'){
	data = read.csv(paste0('../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_', lag, '_withMMBIAS.dat'), sep = ',', header = TRUE)[, c(1, 2, 4)]

	weights = data[, 3]

	weights[weights < 0] = 0

	weights[is.na(weights)] = 0
}

cat(sprintf('\nThe min and max weights are %f and %f.\nThe mean weight is %f and the median weight is %f.\n\n', min(weights), max(weights), mean(weights), median(weights)))

cat(quantile(weights, probs = seq(0, 1, by = 0.05)))

# hist(weights, breaks = 1000)

is.increasing = FALSE

if (is.increasing){
	weights.sort = order(weights)
} else {
	weights.sort = order(weights, decreasing = TRUE)
}

stop.ind = 1000

# Kludge-y way to see how many of the top stop.ind edges
# are reciprocal:

# data[weights.sort[seq(1, stop.ind, by = 2)],3] - data[weights.sort[seq(2, stop.ind, by = 2)],3]

# Look at the top stop.ind edges.

data[weights.sort[1:stop.ind], ]

col.names = c('from_id', 'to_id', 'weight')

if (weight.type == 'hashtag'){
	write.table(data[weights.sort[1:stop.ind], ], file = '../data/topK_hashtag.dat', quote = FALSE, row.names = FALSE, col.names = col.names)
} else if (weight.type == 'mention-retweet'){
	write.table(data[weights.sort[1:stop.ind], ], file = '../data/topK_mention-retweet.dat', quote = FALSE, row.names = FALSE, col.names = col.names)
} else if (weight.type == 'transfer-entropy'){
	write.table(data[weights.sort[1:stop.ind], ], file = '../data/topK_transfer-entropy.dat', quote = FALSE, row.names = FALSE, col.names = col.names)
}

# hist(weights, breaks = 10000, xlim = c(0, 0.1), xlab = paste0('Lag-', lag, ' Transfer Entropy'), ylab = 'Empirical Distribution', freq = FALSE, main = '')

# pdf(paste0('dist_weights_', weight.type, '-', lag, '.pdf'))
# hist(weights, breaks = 10000, xlim = c(0, 0.1), xlab = paste0('Lag-', lag, ' Transfer Entropy'), ylab = 'Empirical Distribution', freq = FALSE, main = '')
# dev.off()