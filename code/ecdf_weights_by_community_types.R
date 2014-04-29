library(np)

kde.positive.support = function(x){
  bwmethod = 'normal-reference'
  # bwmethod = 'cv.ml'
  # bwmethod = 'cv.ls'
  
  bw = npudensbw(~x, bwmethod = bwmethod)
  fhat = npudens(bw)
  
  dt = (max(x)-min(x))/999

  x.eval = seq(min(x), max(x), by = dt)
  
  y = log(x)
  
  bw.y = npudensbw(~y, bwmethod = bwmethod)
  
  trans.x = log(x.eval)
  
  fhat.trimmed = fitted(npudens(edat = trans.x, bws=bw.y))/x.eval
  
  out = list(x.eval = x.eval, fhat = fhat.trimmed)
  
  return(out)
}

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

# label_types = c('struc', 'TE4', 'hashtag', 'mention-retweet')
# weight_types = c('TE4', 'hashtag', 'mention-retweet')

label_types = c('mention-retweet')
weight_types = c('TE4')
# weight_types = c('hashtag')

comms = 0:9

for (label_type in label_types){
for (weight_type in weight_types){

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

	# For some reason min is behaving strangely here...

	min1 = log10(min(data_i.to.i)); min2 = log10(min(data_e.to.i)); min3 = log10(min(data_i.to.e))

	# xmax = 0.05
	xmax = max(c(data_i.to.i, data_e.to.i, data_i.to.e))
# 	xmin = 10^(min(c(min1, min2, min3)))
	xmin = 10^(min(c(min1, min2, min3)))
	if (xmin == 0.){
		xmin = 1e-10
	}

	cat(sprintf('\n\nUsing xmin = %e and xmax = %e\n\n', xmin, xmax))

	# pdf(paste0('figures/', prefix, '_i-to-i-ecdf.pdf'))
	# plot(ecdf(data_i.to.i), xlim = c(0, xmax), xlab = 'Weight', ylab = 'ECDF', main = '')
	# dev.off()

	# pdf(paste0('figures/', prefix, '_e-to-i-ecdf.pdf'))
	# plot(ecdf(data_e.to.i), xlim = c(0, xmax), xlab = 'Weight', ylab = 'ECDF', main = '')
	# dev.off()

	# pdf(paste0('figures/', prefix, '_i-to-e-ecdf.pdf'))
	# plot(ecdf(data_i.to.e), xlim = c(0, xmax), xlab = 'Weight', ylab = 'ECDF', main = '')
	# dev.off()

	lwd = 2

	pdf(paste0('figures/', prefix, '-ecdf.pdf'))
	par(mar=c(4.5,5,2,1), cex.lab = 2, cex.axis = 2)
	plot(ecdf(data_i.to.i), xlim = c(xmin, xmax), xlab = 'Weight', ylab = 'Empirical Distribution of Weights', main = '', col = 'red', lwd = lwd, log = 'x')
	lines(ecdf(data_e.to.i), xlim = c(xmin, xmax), col = 'blue', lwd = lwd)
	lines(ecdf(data_i.to.e), xlim = c(xmin, xmax), col = 'green', lwd = lwd)
	abline(v = c(median(data_i.to.i), median(data_e.to.i), median(data_i.to.e)), col = c('red', 'blue', 'green'), lwd = lwd, lty = rep(2, 3)); 
	legend('topleft', c('Internal-to-Internal', 'External-to-Internal', 'Internal-to-External'), col = c('red', 'blue', 'green'), lwd = lwd, lty = rep(1, 3))
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

	cat(sprintf('\n\nFor %s community %g:\n\nThe mean %s weights internal-to-internal, external-to-internal, and internal-to-external are\n%f\n%f\n%f\n\n', label_type, comm_label, weight_type, mean(data_i.to.i), mean(data_e.to.i), mean(data_i.to.e)))

	cat(sprintf('\n\nFor %s community %g:\n\nThe median %s weights internal-to-internal, external-to-internal, and internal-to-external are\n%f\n%f\n%f\n\n', label_type, comm_label, weight_type, median(data_i.to.i), median(data_e.to.i), median(data_i.to.e)))

	# For mention-retweet, we have to deal with a *lot* of zero weights.

	# if (weight_type == 'mention-retweet'){
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
		
	# }

	# dat <- data.frame(xx = c(data_i.to.i, data_e.to.i, data_i.to.e),yy = c(rep(letters[1], length(data_i.to.i)), rep(letters[2], length(data_e.to.i)), rep(letters[3], length(data_i.to.e))))
	dat <- data.frame(xx = c(data_i.to.i, data_e.to.i, data_i.to.e),Type = c(rep('Internal-to-Internal', length(data_i.to.i)), rep('External-to-Internal', length(data_e.to.i)), rep('Internal-to-External', length(data_i.to.e))))

	# Get factors in the correct order.

	dat$Type = factor(dat$Type, levels = c('Internal-to-Internal', 'External-to-Internal', 'Internal-to-External'))

	breaks = 100

	binwidth = (max(data_all)-min(data_all))/breaks

	# ggplot(dat,aes(x=xx)) + 
	    # geom_histogram(data=subset(dat,yy == 'a'),fill = "red", alpha = 0.5, aes(y=..density..), binwidth = (max(data_i.to.i) - min(data_i.to.i))/breaks) +
	    # geom_histogram(data=subset(dat,yy == 'b'),fill = "blue", alpha = 0.5, aes(y=..density..), binwidth = (max(data_e.to.i) - min(data_e.to.i))/breaks) +
	    # geom_histogram(data=subset(dat,yy == 'c'),fill = "green", alpha = 0.5, aes(y=..density..), binwidth = (max(data_i.to.e) - min(data_i.to.e))/breaks) +
	    # geom_histogram(data=subset(dat,yy == 'a'),fill = "red", alpha = 0.5, aes(y=..density..), binwidth = binwidth) +
	    # geom_histogram(data=subset(dat,yy == 'b'),fill = "blue", alpha = 0.5, aes(y=..density..), binwidth = binwidth) +
	    # geom_histogram(data=subset(dat,yy == 'c'),fill = "green", alpha = 0.5, aes(y=..density..), binwidth = binwidth) +
	    # xlab('Weight') + ylab('Estimated Density') #+
	    # scale_x_log10()
	    # xlim(c(0, 0.05))

	   #  if (weight_type == 'hashtag'){
	   #  	qplot(xx, ..density.., data = dat, geom = "histogram", facets = Type ~ ., binwidth = binwidth, col = Type, fill = Type, xlab = 'Weights', ylab = 'Estimated Density', log = 'x')
	   #  } else{
	   #  	qplot(xx, ..density.., data = dat, geom = "histogram", facets = Type ~ ., binwidth = binwidth, col = Type, fill = Type, xlab = 'Weights', ylab = 'Estimated Density')
	   #  }
    # ggsave(paste0('figures/', prefix, '-hist.pdf'))

  #   if ((length(data_i.to.i[data_i.to.i != 0])!=0)&(length(data_e.to.i[data_e.to.i != 0])!=0)&(length(data_i.to.e[data_i.to.e != 0])!=0)){
  # #   	ggplot(dat,aes(x=xx)) + 
	 # #    geom_density(data=subset(dat,yy == 'a'),color = "red", fill = NA, alpha = 0.2) +
	 # #    geom_density(data=subset(dat,yy == 'b'),color = "blue", fill = NA, alpha = 0.2) +
	 # #    geom_density(data=subset(dat,yy == 'c'),color = "green", fill = NA, alpha = 0.2) +
	 # #    xlab('Weight') + ylab('Estimated Density') #+
	 # #    # scale_x_log10()
	 # #    # xlim(c(0, 0.05))
		# # ggsave(paste0('figures/', prefix, '-dens.pdf'))

		# out_i.to.i = kde.positive.support(data_i.to.i)
		# out_e.to.i = kde.positive.support(data_e.to.i)
		# out_i.to.e = kde.positive.support(data_i.to.e)

		# pdf(paste0('figures/', prefix, '-dens.pdf'))
		# par(mar=c(4.5,4.5,2,1), cex.lab = 2, cex.axis = 2); lwd = 3
		# plot(out_i.to.i$x.eval, out_i.to.i$fhat, type = 'l', col = 'red', xlab = 'Weight', ylab = 'Estimated Density', lwd = lwd)
		# lines(out_e.to.i$x.eval, out_e.to.i$fhat, type = 'l', col = 'blue', lwd = lwd)
		# lines(out_i.to.e$x.eval, out_i.to.e$fhat, type = 'l', col = 'green', lwd = lwd)
		# dev.off()
  #   }
}   
}	
}