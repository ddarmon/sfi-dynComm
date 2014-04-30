# Use Greg Ver Steeg's entropy estimation package to
# compute the Jensen-Shannon divergence between the
# edge distributions.
#
# DMD, 29 April 2014

import entropy_estimators as ee
import math

label_types = ['struc', 'TE4', 'hashtag', 'mention-retweet']
weight_types = ['TE4', 'hashtag', 'mention-retweet']

print 'Label Type\tWeight Type\tD(inter, intra)'

for label_type in label_types:
	for weight_type in weight_types:
		data_inter = []
		data_intra = []
		data_multi = []

		prefix = 'interintramulti_labels-{}_weights-{}'.format(label_type, weight_type)

		with open('../data/edges-by-type/{}_inter.dat'.format(prefix)) as ofile:
			for line in ofile:
				val = float(line)

				if val == 0 or math.isnan(val):
					pass
				else:
					data_inter.append([val])

		with open('../data/edges-by-type/{}_intra.dat'.format(prefix)) as ofile:
			for line in ofile:
				val = float(line)

				if val == 0 or math.isnan(val):
					pass
				else:
					data_intra.append([float(line)])

		with open('../data/edges-by-type/{}_multi.dat'.format(prefix)) as ofile:
			for line in ofile:
				val = float(line)

				if val == 0 or math.isnan(val):
					pass
				else:
					data_multi.append([float(line)])

		K = 5

		KLxy = ee.kldiv(data_inter[:5000], data_intra[:5000], k = K)

		KLyx = ee.kldiv(data_intra[:5000], data_inter[:5000], k = K)

		JS = 0.5*(KLxy + KLyx)

		print label_type, weight_type, JS