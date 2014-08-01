

cat(sprintf('comm\tsum intra\tmean intra\tsum inter\tmean inter\tmore in than out\n'))

for (comm.ind in 1:6){
	weight.type = sprintf('TE%g', comm.ind)

	comm.type = sprintf('TE%g', comm.ind) # Need to change these *together*.
	comm.type.num = comm.ind

	comm.sizes = read.csv(sprintf('../data/coverings/communities%g_comp_sizes.txt', comm.type.num), header = FALSE)$V1

	num.comms = length(comm.sizes[comm.sizes > 2])

	more.in.than.out = rep(0, num.comms)

	for (comm.ind in 0:(num.comms-1)){
		intra = read.csv(sprintf('../data/edges-by-type/interintramulti_labels-%s_weights-%s_comm%g_intra.dat', weight.type, comm.type, comm.ind), header = FALSE)$V1
	
		inter.in = read.csv(sprintf('../data/edges-by-type/interintramulti_labels-%s_weights-%s_comm%g_inter_in.dat', weight.type, comm.type, comm.ind), header = FALSE)$V1
		inter.out = read.csv(sprintf('../data/edges-by-type/interintramulti_labels-%s_weights-%s_comm%g_inter_out.dat', weight.type, comm.type, comm.ind), header = FALSE)$V1
	
		# inter = inter.in
		# inter = inter.out
		inter = c(inter.in, inter.out)
	
		inter = inter[!is.na(inter)]; intra = intra[!is.na(intra)]
	
		if (median(intra, na.rm = TRUE) > median(inter, na.rm = TRUE)){
		# if (mean(intra, na.rm = TRUE) > mean(inter, na.rm = TRUE)){
			more.in.than.out[comm.ind + 1] = 1
		}
	
		pdf(sprintf('figures/interintra/interintramulti_labels-%s_weights-%s_comm%g.pdf', weight.type, comm.type, comm.ind))
		plot(density(intra, from = 0), col = 'red')
		lines(density(inter, from = 0), col = 'blue')
		legend('topright', legend = c(sprintf('Intra, n = %g', length(intra)), sprintf('Inter, n = %g', length(inter))), col = c('red', 'blue'), lty = 1)
		dev.off()
	
		cat(sprintf('%g\t%g\t%g\t%g\t%g\t%g\n',comm.ind, sum(intra, na.rm = TRUE), mean(intra, na.rm = TRUE), sum(inter, na.rm = TRUE), mean(inter, na.rm = TRUE), more.in.than.out[comm.ind + 1]))
	}

	cat(sprintf('\n\nOf the %g communities, %f have greater average internal compared to average external weighted degree.\n\n', num.comms, mean(more.in.than.out)))
}
