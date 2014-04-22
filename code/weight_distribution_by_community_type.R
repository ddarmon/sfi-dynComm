# A script that computes the distribution of 
# i-to-i, e-to-i, and i-to-e weights *across
# communities*. Compare this to 
#
# 	analyze_weights_by_community_types.R
# 
# which does this individually for *each*
# community.
#
# DMD, 22 April 2014

# Search type to use:
# 	labels-BLANK_weights-BLANK
#
# Ex: labels-struc_weights-TE4

# label_type = 'struc'
# label_type = 'TE4'
# label_type = 'hashtag'
# label_type = 'mention-retweet'

# weight_type = 'TE4'
# weight_type = 'hashtag'
# weight_type = 'mention-retweet'

label_types = c('struc', 'TE4', 'hashtag', 'mention-retweet')
weight_types = c('TE4', 'hashtag', 'mention-retweet')

# label_types = c('struc')
# label_types = c('TE4')
# label_types = c('hashtag')
# label_types = c('mention-retweet')

# weight_types = c('TE4')
# weight_types = c('hashtag')
# weight_types = c('mention-retweet')

comms = c(0:19)

for (label_type in label_types){
for (weight_type in weight_types){

data_e.to.i_aggregate = c()
data_i.to.e_aggregate = c()
data_i.to.i_aggregate = c()

for (comm_label in comms){
# for (comm_label in c(0)){
	prefix = paste0('comm', comm_label, '_labels-', label_type, '_weights-', weight_type)

	data_i.to.i = read.csv(paste0('../data/edges-by-type/', prefix, '_i-to-i.dat'), header = FALSE)$V1
	data_e.to.i = read.csv(paste0('../data/edges-by-type/', prefix, '_e-to-i.dat'), header = FALSE)$V1
	data_i.to.e = read.csv(paste0('../data/edges-by-type/', prefix, '_i-to-e.dat'), header = FALSE)$V1

	# Deal with NAs

	data_i.to.i[is.na(data_i.to.i)] = 0
	data_e.to.i[is.na(data_e.to.i)] = 0
	data_i.to.e[is.na(data_i.to.e)] = 0

	data_i.to.i_aggregate = c(data_i.to.i_aggregate, data_i.to.i)
	data_e.to.i_aggregate = c(data_e.to.i_aggregate, data_e.to.i)
	data_i.to.e_aggregate = c(data_i.to.e_aggregate, data_i.to.e)
}

if (weight_type == 'mention-retweet'){
	cat(sprintf('\n\n\n\n\n!!!Warning: Removing 0 edges!!!!\n\n\n\n\n'))

	which_i.to.i = which(data_i.to.i_aggregate == 0)
	if (length(which_i.to.i > 0)){
		data_i.to.i_aggregate = data_i.to.i_aggregate[-which_i.to.i]
	}

	which_e.to.i = which(data_e.to.i_aggregate == 0)
	if (length(which_e.to.i > 0)){
		data_e.to.i_aggregate = data_e.to.i_aggregate[-which_e.to.i]
	}

	which_i.to.e = which(data_i.to.e_aggregate == 0)
	if (length(which_i.to.e > 0)){
		data_i.to.e_aggregate = data_i.to.e_aggregate[-which_i.to.e]
	}
}

data.all = c(data_i.to.i_aggregate, data_e.to.i_aggregate, data_i.to.e_aggregate)

if (weight_type == 'TE4'){
	xlim = c(0, 0.03)
}else if (weight_type == 'hashtag'){
	xlim = c(0, 0.1)
}else{
	xlim = range(data.all)
}

ab.lw = 3
ecdf.lw = 3

prefix.pdf = paste0('labels-', label_type, '_weights-', weight_type)

pdf(paste0('figures/', prefix.pdf, '-ecdf_by_type.pdf'))
par(mar=c(5,6,2,1), cex.lab = 2, cex.axis = 2)
plot(ecdf(data_i.to.i_aggregate), col = 'red', xlim = xlim, ylab = expression(paste('P(', W[i*j] <= w, '| ', T == t, ')')), xlab = expression(paste('Weight, ', w)), lw = ecdf.lw, main = sprintf('Community Type %s, Weight Type %s', label_type, weight_type), lty = 1)
lines(ecdf(data_e.to.i_aggregate), col = 'blue', lw = ecdf.lw, lty = 2)
lines(ecdf(data_i.to.e_aggregate), col = 'green', lw = ecdf.lw, lty = 3)
legend('bottomright', legend = c('Internal-to-Internal', 'External-to-Internal', 'Internal-to-External'), col = c('red', 'blue', 'green'), lty = 1:3, lw = ecdf.lw)
abline(v = median(data_i.to.i_aggregate), col = 'red', lw = ab.lw, lty = 1)
abline(v = median(data_e.to.i_aggregate), col = 'blue', lw = ab.lw, lty = 2)
abline(v = median(data_i.to.e_aggregate), col = 'green', lw = ab.lw, lty = 3)
dev.off()

}	
}

