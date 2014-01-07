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

lag = '6'
prefix = 'edge_weights_bin10minutes_lag_{}_withMMBIAS_edgelist.dat_oslo_files'.format(lag)

# fname = '{}/tp'.format(prefix)
fname = '{}/tp_without_singletons'.format(prefix)

comm_dict = {} # A dictionary of the form {communityid : nodes}
comm_count = 0

node_dict = {} # A dictionary of the form {nodeid : communities}

with open(fname) as ofile:
	line = ofile.readline()

	while line != '':
		nodes = ofile.readline().strip().split(' ')
		comm_dict[comm_count] = nodes

		for node in nodes:
			if node in node_dict:
				node_dict[node].append(comm_count)
			else:
				node_dict[node] = [comm_count]

		comm_count += 1

		line = ofile.readline()

userid_to_username = {}

with open('/Users/daviddarmon/Documents/Reference/R/Research/2013/network/tweetpredict/user_lookup/user_lookups/user_lookup-2011.tsv') as ofile:
	for line in islice(ofile, 1, None): # Skip the first line, which is a header line
		uid, username = line.strip().split('\t')

		userid_to_username[uid] = username

num_overlap = 0

for nodeid in node_dict:
	comms = node_dict[nodeid]

	if len(comms) > 1:
		print len(comms), userid_to_username[nodeid], comms

		num_overlap += 1

print 'There are {} users that belong to more than one community, of {}.'.format(num_overlap, len(node_dict))