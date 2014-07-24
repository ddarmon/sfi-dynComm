cat(sprintf('comm\tsum intra\tmean intra\tsum inter\tmean inter\tmore in than out\n'))

num.comms = 100

more.in.than.out = rep(0, num.comms)

for (comm.ind in 0:(num.comms-1)){
	intra = read.csv(sprintf('../data/edges-by-type/interintramulti_labels-TE4_weights-TE4_comm%g_intra.dat', comm.ind), header = FALSE)$V1
	
	# inter = read.csv(sprintf('../data/edges-by-type/interintramulti_labels-TE4_weights-TE4_comm%g_inter_in.dat', comm.ind), header = FALSE)$V1
	inter = read.csv(sprintf('../data/edges-by-type/interintramulti_labels-TE4_weights-TE4_comm%g_inter_out.dat', comm.ind), header = FALSE)$V1
	
	if (mean(intra, na.rm = TRUE) > mean(inter, na.rm = TRUE)){
		more.in.than.out[comm.ind + 1] = 1
	}
	
	cat(sprintf('%g\t%g\t%g\t%g\t%g\t%g\n',comm.ind, sum(intra, na.rm = TRUE), mean(intra, na.rm = TRUE), sum(inter, na.rm = TRUE), mean(inter, na.rm = TRUE), more.in.than.out[comm.ind + 1]))
}

