# A script to count the number of 
# intra-, inter-, and multi-edges
# induced by each community type.

# DMD, 6 May 2014

import sys
import numpy

output = sys.stdout

weight_type = 'hashtag'

for label_type in ['struc', 'TE4', 'hashtag', 'mention-retweet']:
	print 'Considering communities defined by {}...'.format(label_type)

	count_edge_types = numpy.zeros(3)

	for edge_ind, edge_type in enumerate(['intra', 'inter', 'multi']):
		prefix = 'interintramulti_labels-{}_weights-{}'.format(label_type, weight_type)

		with open('../data/edges-by-type/{}_{}.dat'.format(prefix, edge_type)) as ofile:
			counter = 0
			for line in ofile:
				counter+=1

			count_edge_types[edge_ind] = counter

		output.write('{}\t{}\t{}\n'.format(counter, label_type, edge_type))

	print 'Total number of edges = {}'.format(int(numpy.sum(count_edge_types)))

	print label_type, count_edge_types/numpy.sum(count_edge_types)

	print ''