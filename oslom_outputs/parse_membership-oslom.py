# A script to parse a file created using OSLOM.

#	DMD, 261213-15-48

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
	full_name = '{}/tp_without_singletons'.format(prefix)

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
		out = open('communities/communitites{}.txt'.format(lag), 'w')
	else:
		out = sys.stdout

	for c_ind in range(len(comm_dict)):
		community = comm_dict[c_ind]

		out.write('Community {} has: \t {} members\n'.format(c_ind, len(community)))

		members = ''

		for member in community:
			members += '{} '.format(userid_to_username.get(member, 'NULL'))

		comm_sizes.append(len(community))

		out.write(members)

		out.write('\n\n')


	ranked_comms = ''

	for comm in numpy.argsort(comm_sizes)[-10:][::-1]:
		ranked_comms = ranked_comms + '{}, '.format(comm)

	print '\n\nFor file {}, the 10 largest communities (from largest to smallest) are [{}].\n\n'.format(prefix, ranked_comms)

	if to_file:
		out.close()

	pylab.figure()
	pylab.bar(range(len(comm_dict)), numpy.sort(comm_sizes)[::-1])
	pylab.xlim(0, len(comm_dict))
	pylab.xlabel('Community Rank')
	pylab.ylabel('Community Size')
	pylab.savefig('figures/comm-oslom{}.pdf'.format(lag))
	pylab.close()