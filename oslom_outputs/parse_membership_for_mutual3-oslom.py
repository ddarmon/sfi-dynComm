# A script to parse a file created using OSLOM to
# be used with mutual from 
#
# 	https://sites.google.com/site/andrealancichinetti/mutual
#

#	DMD, 291213-22-21

import pylab
import numpy
from itertools import islice
import sys

# All of the communities (or 'modules') are
# written into the 'tp' files, which have the format
# 
# # module n size: N bs: sig_val
# # node1, node2, node3, ...

weighted_prefixes = ['edge_weights_bin10minutes_lag_{}_withMMBIAS_edgelist.dat_oslo_files'.format(lag) for lag in range(1, 7)]

prefixes = ['twitter_unweighted_network.txt_oslo_files']

prefixes.extend(weighted_prefixes)

prefixes.extend(['twitter_network_hashtags_weighted.txt_oslo_files', 'twitter_network_contentfull_weighted_arithmeticmean.txt_oslo_files'])

for lag, prefix in enumerate(prefixes):
	# full_name = '{}/tp_without_singletons'.format(prefix)
	full_name = '{}/tp'.format(prefix)

	comm_dict = {}
	comm_count = 0

	with open(full_name) as ofile:
		line = ofile.readline()

		while line != '':
			nodes = ofile.readline().strip().split(' ')
			comm_dict[comm_count] = nodes

			comm_count += 1

			line = ofile.readline()

	userid_to_username = {}

	with open('/Users/daviddarmon/Documents/Reference/R/Research/2013/network/tweetpredict/user_lookup/user_lookups/user_lookup-2011.tsv') as ofile:
		for line in islice(ofile, 1, None): # Skip the first line, which is a header line
			uid, username = line.strip().split('\t')

			userid_to_username[uid] = username

	comm_sizes = []

	to_file = True

	if to_file:
		out = open('communities/communitites{}_comp.txt'.format(lag), 'w')
	else:
		out = sys.stdout

	for c_ind in range(len(comm_dict)):
		community = comm_dict[c_ind]

		members = ''

		for member in community:
			members += '{} '.format(member)

		out.write(members)

		out.write('\n')

	if to_file:
		out.close()