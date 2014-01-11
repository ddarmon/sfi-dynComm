# A script to generate the size distributions for the 
# various community types.

file.inds = c(0, 4, 7, 8)

colors = c('black', 'blue', 'red', 'darkgreen')

lwd = 2

max.comm.size = 811

pdf(sprintf('figures/comm_sizes_ecdf.pdf'))
par(mar=c(4.5,5,2,1), cex.lab = 2, cex.axis = 2)
plot(0, cex = 0, log = 'xy', type = 'l', xlim = c(1, max.comm.size), ylim = c(1e-4, 0.5), xlab = 'c', ylab = 'Proportion of communities larger than c')

for (cur.ind in 1:4){
	cat(sprintf('\n\n====\n\n'))
	file.ind = file.inds[cur.ind]

	inputFile = sprintf("mutual3/coverings/singletons/communitites%g_comp.txt", file.ind)
	con  = file(inputFile, open = "r")

	comm.sizes = integer()

	oneLine = readLines(con, n = 1, warn = FALSE)

	while (length(oneLine) > 0) {
	    nodes = strsplit(oneLine, " ")
	    
	    comm.sizes = c(comm.sizes, length(nodes[[1]]))

	    oneLine = readLines(con, n = 1, warn = FALSE)
	  } 

	close(con)

	counts = table(comm.sizes)
	counts.without.singletons = counts[2:length(counts)]

	cat(sprintf('%g\n\n', max(comm.sizes)))
	cat(sprintf('Max size of community: %g\n\n', max(comm.sizes)))
	cat(sprintf('Proportion %f of communities are size 1\n\n', counts[1]/sum(counts)))
	cat(sprintf('%g are singletons.\n\n', counts[1]))

	# pdf(sprintf('figures/comm%gsize_dist.pdf', file.ind))
	# par(mar=c(4,4.5,2,1), cex.lab = 2, cex.axis = 2)
	# plot(as.numeric(names(counts.without.singletons)), counts.without.singletons, type = 'h', log = 'y', xlim = c(0, 900), xlab = 'Size of Community', ylab = 'Proportion of Communities')
	# dev.off()

	# F = ecdf(counts.without.singletons)
	# x = seq(min(counts.without.singletons), 800, by = 0.01)

	F = ecdf(comm.sizes)
	x = seq(1, max(comm.sizes), by = 0.01)

	cat(sprintf('%f\n\n', min(1-F(x))))

	lines(x, 1 - F(x), col = colors[cur.ind], lwd = lwd)
}
legend('topright', c('Structural', 'Activity-based', 'Content-based', 'Interaction-based'), lwd = rep(lwd,4), lty = rep(1, 4), col = colors)
dev.off()