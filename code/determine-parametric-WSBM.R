library(MASS)

edge.types = c('e-to-i', 'i-to-e', 'i-to-i')

label.types = c('struc', 'TE4', 'hashtag', 'mention-retweet')
label.type = label.types[2]
weight.types = c('blank', 'TE4', 'hashtag', 'mention-retweet')
weight.type = weight.types[2]

weight.dists = c('lognormal', 'gamma', 'exponential', 'pareto')
weight.dist = weight.dists[2]

# method.type = '' # For OSLOM
method.type = 'WSBM_K4' # For WSBM

# comm.ranks = c(1)
comm.ranks = 0:3

for (comm.rank in comm.ranks){
	par(mar=c(5,5,2,1), cex.lab = 2, cex.axis = 2, mfrow = c(3, 1))
	for (edge.type in edge.types){
		input.fname = sprintf('../data/edges-by-type/comm%g%s_labels-%s_weights-%s_%s.dat', comm.rank, method.type, label.type, weight.type, edge.type)
	
		data = read.csv(input.fname, header = FALSE)$V1
		which.na = is.na(data)

		if (sum(which.na > 0)){
			cat(sprintf('Warning: There are NAN that we are removing.\n\n'))
	
			data = data[!which.na]
		}
		
		is.neg = (data <= 0)
		
		if (sum(is.neg) > 0){
			cat(sprintf('Warning: There are negative values that we are removing.\n\n'))
			
			data = data[!is.neg]
		}
	
		median.weight = median(data)
	
		cat(sprintf('There are %g %s type edges.\n', length(data), edge.type))
		cat(sprintf('The median %s type weight is %f.\n', edge.type, median.weight))
		
		if (weight.type == 'TE4'){
			xlim = c(0, 0.1); ylim = c(0, 500)
		} else if (weight.type == 'hashtag'){
			xlim = c(0, 0.1); ylim = c(0, 1500)
		} else if (weight.type == 'mention-retweet'){
			xlim = c(0, 0.1); ylim = c(0, 400)
		}
		
		plot(density(data, from = 0), xlim = xlim, ylim = ylim, main = sprintf('Edge Type: %s, Num Edges = %g, Median Weight = %f', edge.type, length(data), median.weight), xlab = 'Weight', ylab = 'Estimated Density', lwd = 3, col = 'red')
		hist(data, add = T, probability = TRUE, breaks = 'Sturges')
		abline(v = median(data), col = 'green', lwd = 3, lty = 2)
		
		if (weight.dist == 'gamma'){
			# Fit a gamma distribution to the data.

			fit.gamma = fitdistr(data, "gamma")
			x = seq(0.001, 0.1, by = 0.0005)
			
			lines(x,dgamma(x, shape = fit.gamma$estimate[1], rate = fit.gamma$estimate[2]), lwd = 3, col = 'blue')
		} else if (weight.dist == 'lognormal'){
			# Fit a lognormal distribution to the data.
			
			mu.hat = sum(log(data))/length(data)
			var.hat = sum((log(data) - mu.hat)^2)/length(data)
			
			cat(sprintf('The mean and variance are %f and %g.\n', mu.hat, var.hat))
			
			x = seq(0.0005, 0.1, by = 0.0005)
			
			lines(x, dlnorm(x, meanlog = mu.hat, sdlog = sqrt(var.hat)), lwd = 3, col = 'blue')
		} else if (weight.dist == 'exponential'){
			# Fit an exponential distribution to the data
			
			lambda.hat = 1/mean(data)
			
			x = seq(0, 0.1, by = 0.0005)
			
			lines(x, dexp(x, rate = lambda.hat), lwd = 3, col = 'blue')
		} else if (weight.dist == 'pareto'){
			# Fit a Pareto distribution to the data.
			
			x.min = min(data)
			alpha.hat = length(data)/sum(log(data) - log(x.min))
			
			source('pareto.R')
			
			my.dpareto = function(x, x.min, alpha){
				return(alpha*x.min^(alpha)/(x^(alpha+1)))
			}
			
			x = seq(0.001, 0.1, by = 0.0005)
			
			lines(x, my.dpareto(x, x.min = x.min, alpha = alpha.hat), lwd = 3, col = 'blue')
		}
	}
}