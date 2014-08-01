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

# library(reldist)

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

output.filename = 'stats_for_edges.dat'

cat('comm.type\tweight.type\tmed.intra\tmed.inter\tmed.multi\tn.intra\tn.inter\tn.multi\n', file = output.filename, append = FALSE)

for (label_type in label_types){
for (weight_type in weight_types){

	cat(sprintf('Working with %s / %s\n\n', label_type, weight_type))

prefix = paste0('interintramulti_labels-', label_type, '_weights-', weight_type)

cat(sprintf('Loading data...\n\n'))

data_inter = read.csv(paste0('../data/edges-by-type/', prefix, '_inter.dat'), header = FALSE)$V1
data_intra = read.csv(paste0('../data/edges-by-type/', prefix, '_intra.dat'), header = FALSE)$V1
data_multi = read.csv(paste0('../data/edges-by-type/', prefix, '_multi.dat'), header = FALSE)$V1

cat(sprintf('Finished loading data...\n\n'))

if ((weight_type == 'mention-retweet') || (weight_type == 'hashtag')){
	cat(sprintf('\n\n\n\n\n!!!Warning: Removing 0 edges!!!!\n\n\n\n\n'))

	which_inter = which(data_inter == 0)
	if (length(which_inter > 0)){
		data_inter = data_inter[-which_inter]
	}

	which_intra = which(data_intra == 0)
	if (length(which_intra > 0)){
		data_intra = data_intra[-which_intra]
	}

	which_multi = which(data_multi == 0)
	if (length(which_multi > 0)){
		data_multi = data_multi[-which_multi]
	}
}

# Remove NAs

data_inter[is.na(data_inter)] = 0
data_intra[is.na(data_intra)] = 0
data_multi[is.na(data_multi)] = 0

if (weight_type == 'TE4'){
	xlim = c(0, 0.03)
}else if (weight_type == 'hashtag'){
	xlim = c(0, 0.1)
}else{
	xlim = range(c(data_inter, data_intra, data_multi))
}

lwd.cdf = 3

prefix.pdf = paste0('labels-', label_type, '_weights-', weight_type)

# pdf(paste0('figures/', prefix.pdf, '-ecdf_by_type.pdf'))
# plot(ecdf(data_inter), col = 'green', ylab = expression(paste('P(', W[i*j] <= w, '| ', T == t, ')')), xlab = expression(paste('Weight, ', w)), lwd = lwd.cdf, main = sprintf('Community Type %s, Weight Type %s', label_type, weight_type), lty = 1, xlim = xlim)
# lines(ecdf(data_intra), col = 'red', lwd = lwd.cdf, lty = 2)
# lines(ecdf(data_multi), col = 'blue', lwd = lwd.cdf, lty = 3)
# legend('bottomright', legend = c('Intra', 'Inter', 'Multi'), col = c('red', 'green', 'blue'), lty = 1:3, lwd = 3)
# dev.off()

to.do.points = FALSE
vertical = FALSE

tiff(paste0('figures/', prefix.pdf, '-ecdf_by_type.tiff'), res = 120)
par(mar=c(5,5,2,2), cex.lab = 2, cex.axis = 2)
main.text = sprintf('Community Type %s, Weight Type %s', label_type, weight_type)
plot(ecdf(data_inter), verticals = vertical, do.points = to.do.points, col = 'blue', ylab = expression(paste('P(', W[i*j] <= w, '| ', T == t, ')')), xlab = expression(paste('Weight, ', w)), lwd = lwd.cdf, main = '', lty = 1, xlim = xlim)
lines(ecdf(data_intra), verticals = vertical, do.points = to.do.points, col = 'red', lwd = lwd.cdf, lty = 2)
lines(ecdf(data_multi), verticals = vertical, do.points = to.do.points, col = 'darkmagenta', lwd = lwd.cdf, lty = 3)
# legend('bottomright', legend = c('Intra', 'Inter', 'Multi'), col = c('blue', 'red', 'darkmagenta'), lty = 1:3, lwd = 3)
dev.off()

fs = c(density(data_inter, from = 0)$y, density(data_intra, from = 0)$y, density(data_multi, from = 0)$y)

if (weight_type == 'TE4'){
	xlim = c(0, 0.04)
	ylim = c(0, 150)
	log  = ''
} else if (weight_type == 'hashtag'){
	xlim = c(0, 0.02)
	# ylim = c(0, max(fs))
	ylim = c(0, 2000)
	log  = ''
} else if (weight_type == 'mention-retweet'){
	xlim = c(0, 0.1)
	ylim = c(0, 80)
	log = ''
}

tiff(paste0('figures/', prefix.pdf, '-pdf_by_type.tiff'), res = 120)
par(mar=c(5,5,2,1), cex.lab = 2, cex.axis = 2)
plot(density(data_inter, from = 0), col = 'blue', xlim = xlim, ylim = ylim, lty = 1, lwd = lwd.cdf, main = '', xlab = expression(paste('Weight, ', w)), ylab = expression(paste('f(', w, '| ', T == t, ')')), log = log)
lines(density(data_intra, from = 0), col = 'red', lty = 2, lwd = lwd.cdf)
lines(density(data_multi, from = 0), col = 'darkmagenta', lty = 3, lwd = lwd.cdf)
# legend('topright', legend = c('Intra', 'Inter', 'Multi'), col = c('blue', 'red', 'darkmagenta'), lty = 1:3, lwd = 3)
dev.off()

# plot(density(data_inter, from = 0), col = 'blue', lty = 1, lwd = lwd.cdf, main = '', xlab = expression(paste('Weight, ', w)), ylab = expression(paste('f(', w, '| ', T == t, ')')))
# lines(density(data_intra, from = 0), col = 'red', lty = 2, lwd = lwd.cdf)
# lines(density(data_multi, from = 0), col = 'darkmagenta', lty = 3, lwd = lwd.cdf)
# legend('topright', legend = c('Intra', 'Inter', 'Multi'), col = c('blue', 'red', 'darkmagenta'), lty = 1:3, lwd = 3)

# dev.off()

cat(sprintf('%s\t%s\t%f\t%f\t%f\t%g\t%g\t%g\n', label_type, weight_type, median(data_intra), median(data_inter), median(data_multi), length(data_intra), length(data_inter), length(data_multi)), file = output.filename, append = TRUE)

}
}

# The density of transfer entropy estimator under the null hypothesis
# of zero transfer entropy.

# dens.x = seq(0, 5, by = 0.01)

# plot(dens.x, dchisq(df = 2, x = dens.x), col = 'black', lwd = 3, type = 'l')