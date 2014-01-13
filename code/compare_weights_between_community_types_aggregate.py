# Get out the change in median weight for in-to-in vs. in/out-to-out/in
# edges.
#
#	DMD, 120114-19-48

import numpy

label_type = 'struc'
weight_type = 'hashtag'
for weight_type in ['TE4', 'mention-retweet', 'hashtag']:
	for label_type in ['struc', 'TE4', 'mention-retweet', 'hashtag']:
		print 'Using the {}/{} pairing.'.format(label_type, weight_type)

		ratio_e_to_i = []
		ratio_i_to_e = []

		for comm_rank in range(100):
			file_prefix = 'comm{}_labels-{}_weights-{}'.format(comm_rank, label_type, weight_type)

			i_to_i = numpy.loadtxt('../data/edges-by-type/{}_i-to-i.dat'.format(file_prefix))
			e_to_i = numpy.loadtxt('../data/edges-by-type/{}_e-to-i.dat'.format(file_prefix))
			i_to_e = numpy.loadtxt('../data/edges-by-type/{}_i-to-e.dat'.format(file_prefix))

			# print 'The i-to-i, e-to-i, and i-to-e medians are {}, {}, {}.'.format(numpy.median(i_to_i), numpy.median(e_to_i), numpy.median(i_to_e))

			if weight_type == 'mention-retweet':
				i_to_i = i_to_i[i_to_i != 0]
				e_to_i = e_to_i[e_to_i != 0]
				i_to_e = i_to_e[i_to_e != 0]

			med_i_to_i = numpy.median(i_to_i)
			med_e_to_i = numpy.median(e_to_i)
			med_i_to_e = numpy.median(i_to_e)

			# print med_i_to_i, med_e_to_i, med_i_to_e

			rat_e_to_i = med_i_to_i/med_e_to_i
			rat_i_to_e = med_i_to_i/med_i_to_e

			print '{}\t{}'.format(rat_e_to_i, rat_i_to_e)

			ratio_e_to_i.append(rat_e_to_i)
			ratio_i_to_e.append(rat_i_to_e)

		print 'The median e-to-i ratio is {} ({}).\nThe median i-to-e ratio is {} ({}).'.format(numpy.median(ratio_e_to_i), numpy.mean(ratio_e_to_i), numpy.median(ratio_i_to_e), numpy.mean(ratio_i_to_e))