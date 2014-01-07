library(np)

# Search type to use:
# 	labels-BLANK_weights-BLANK
#
# Ex: labels-struc_weights-TE4

# label_type = 'struc'
# label_type = 'TE4'
# label_type = 'hashtag'
label_type = 'mention-retweet'

weight_type = 'TE4'
# weight_type = 'hashtag'
# weight_type = 'mention-retweet'

comms = 0:9

for (comm_label in comms){
	prefix = paste0('comm', comm_label, '_labels-', label_type, '_weights-', weight_type)

	data_i.to.i = read.csv(paste0('../data/edges-by-type/', prefix, '_i-to-i.dat'), header = FALSE)$V1

	data_e.to.i = read.csv(paste0('../data/edges-by-type/', prefix, '_e-to-i.dat'), header = FALSE)$V1

	data_i.to.e = read.csv(paste0('../data/edges-by-type/', prefix, '_i-to-e.dat'), header = FALSE)$V1

	# Deal with NAs

	data_i.to.i[is.na(data_i.to.i)] = 0
	data_e.to.i[is.na(data_e.to.i)] = 0
	data_i.to.e[is.na(data_i.to.e)] = 0

	# xmax = 0.2
	xmax = max(c(data_i.to.i, data_e.to.i, data_i.to.e))

	pdf(paste0('figures/', prefix, '_i-to-i-ecdf.pdf'))
	plot(ecdf(data_i.to.i), xlim = c(0, xmax), xlab = 'Weight', ylab = 'ECDF', main = '')
	dev.off()

	pdf(paste0('figures/', prefix, '_e-to-i-ecdf.pdf'))
	plot(ecdf(data_e.to.i), xlim = c(0, xmax), xlab = 'Weight', ylab = 'ECDF', main = '')
	dev.off()

	pdf(paste0('figures/', prefix, '_i-to-e-ecdf.pdf'))
	plot(ecdf(data_i.to.e), xlim = c(0, xmax), xlab = 'Weight', ylab = 'ECDF', main = '')
	dev.off()

	# pdf(paste0('figures/', prefix, '-dens.pdf'))
	# plot(density(data_i.to.i[data_i.to.i != 0]), col = 'red', xlab = 'Weight', ylab = 'Estimated Density', main = '')#, xlim = c(0, 0.006))
	# lines(density(data_e.to.i[data_e.to.i != 0]), col = 'blue')
	# lines(density(data_i.to.e[data_i.to.e != 0]), col = 'green')
	# legend('topright', c('Internal-to-Internal', 'External-to-Internal', 'Internal-to-External'), col = c('red', 'blue', 'green'), lty = rep(1, 3))
	# dev.off()

	data_all = c(data_i.to.i, data_e.to.i, data_i.to.e)

	# hist(data_i.to.i, col = 'red', freq = TRUE, main = '', xlim = c(min(data_all), max(data_all)))
	# hist(data_e.to.i, col = 'blue', freq = TRUE, add = T)
	# hist(data_i.to.e, col = 'green', freq = TRUE, add = T)

	# Use ggplot to make the densities.

	library(ggplot2)

	cat(sprintf('\n\nFor community %g:\n\nThe mean %s weights internal-to-internal, external-to-internal, and internal-to-external are\n%f\n%f\n%f\n\n', comm_label, weight_type, mean(data_i.to.i), mean(data_e.to.i), mean(data_i.to.e)))

	# For mention-retweet, we have to deal with a *lot* of zero weights.

	if (weight_type == 'mention-retweet'){
		num.nonzero_i.to.i = sum(data_i.to.i != 0)
		num.nonzero_e.to.i = sum(data_e.to.i != 0)
		num.nonzero_i.to.e = sum(data_i.to.e != 0)

		cat(sprintf('\n\nThere were\n%g of %g (%f) nonzero internal-to-internal edges,\n%g of %g (%f) nonzero external-to-internal edges, and\n%g of %g (%f) nonzero internal-to-external edges.\n\n', num.nonzero_i.to.i, length(data_i.to.i), num.nonzero_i.to.i/length(data_i.to.i), num.nonzero_e.to.i, length(data_e.to.i), num.nonzero_e.to.i/length(data_e.to.i), num.nonzero_i.to.e, length(data_i.to.e), num.nonzero_i.to.e/length(data_i.to.e)))

		if ((num.nonzero_i.to.i != length(data_i.to.i))&(num.nonzero_i.to.i != 0)){
			data_i.to.i = data_i.to.i[-which(data_i.to.i == 0)]
		}

		if ((num.nonzero_e.to.i != length(data_e.to.i))&(num.nonzero_e.to.i != 0)){
			data_e.to.i = data_e.to.i[-which(data_e.to.i == 0)]
		}

		if ((num.nonzero_i.to.e != length(data_i.to.e))&(num.nonzero_i.to.e != 0)){
			data_i.to.e = data_i.to.e[-which(data_i.to.e == 0)]
		}
		
	}

	dat <- data.frame(xx = c(data_i.to.i, data_e.to.i, data_i.to.e),yy = c(rep(letters[1], length(data_i.to.i)), rep(letters[2], length(data_e.to.i)), rep(letters[3], length(data_i.to.e))))

	breaks = 50

	binwidth = (max(data_all)-min(data_all))/breaks

	ggplot(dat,aes(x=xx)) + 
	    # geom_histogram(data=subset(dat,yy == 'a'),fill = "red", alpha = 0.5, aes(y=..density..), binwidth = (max(data_i.to.i) - min(data_i.to.i))/breaks) +
	    # geom_histogram(data=subset(dat,yy == 'b'),fill = "blue", alpha = 0.5, aes(y=..density..), binwidth = (max(data_e.to.i) - min(data_e.to.i))/breaks) +
	    # geom_histogram(data=subset(dat,yy == 'c'),fill = "green", alpha = 0.5, aes(y=..density..), binwidth = (max(data_i.to.e) - min(data_i.to.e))/breaks) +
	    geom_histogram(data=subset(dat,yy == 'a'),fill = "red", alpha = 0.5, aes(y=..density..), binwidth = binwidth) +
	    geom_histogram(data=subset(dat,yy == 'b'),fill = "blue", alpha = 0.5, aes(y=..density..), binwidth = binwidth) +
	    geom_histogram(data=subset(dat,yy == 'c'),fill = "green", alpha = 0.5, aes(y=..density..), binwidth = binwidth) +
	    xlab('Weight') + ylab('Estimated Density') #+ 
	    # scale_x_log10()
	    # xlim(c(0, 0.05))
    ggsave(paste0('figures/', prefix, '-hist.pdf'))
    show((length(data_i.to.i[data_i.to.i != 0])!=0)&(length(data_e.to.i[data_e.to.i != 0])!=0)&(length(data_i.to.e[data_i.to.e != 0])!=0))
    if ((length(data_i.to.i[data_i.to.i != 0])!=0)&(length(data_e.to.i[data_e.to.i != 0])!=0)&(length(data_i.to.e[data_i.to.e != 0])!=0)){
    	ggplot(dat,aes(x=xx)) + 
	    geom_density(data=subset(dat,yy == 'a'),color = "red", fill = NA, alpha = 0.2) +
	    geom_density(data=subset(dat,yy == 'b'),color = "blue", fill = NA, alpha = 0.2) +
	    geom_density(data=subset(dat,yy == 'c'),color = "green", fill = NA, alpha = 0.2) +
	    xlab('Weight') + ylab('Estimated Density') #+
	    # scale_x_log10()
	    # xlim(c(0, 0.05))
		ggsave(paste0('figures/', prefix, '-dens.pdf'))
    }
    
	
}