# A script that takes as an input a .map file as produced by Infomap
# and outputs a list of the userids grouped into communities.
#
# DMD, 9 May 2014

from itertools import islice
import numpy

type_to_name = {0 : 'twitter_unweighted_network_idsfrom1',
				4 : 'edge_weights_bin10minutes_lag_4_withMMBIAS_edgelist_idsfrom1',
				7 : 'twitter_network_hashtags_weighted_idsfrom1',
				10: 'twitter_network_contentfull_weighted_arithmeticmean_idsfrom1'}

# A dictionary that takes in a lookup value and 
# outputs the associated userid

lookup_to_userid = {}

fname = '/Users/daviddarmon/Documents/Reference/R/Research/2013/sfi-dynComm/Infomap-0.15.1/results/new_ids_dictionary.txt'

with open(fname) as ofile:
	for line in islice(ofile, 1, None):
		userid, lookupid = map(int, line.split('\t'))

		lookup_to_userid[lookupid] = userid

comm_types = [0, 4, 7, 10]

for comm_type in comm_types:
	# A dictionary that takes in a community id (starting
	# at 1) and outputs the list of users (by id).

	comms_to_users = {}

	dir_prefix   = '/Users/daviddarmon/Documents/Reference/R/Research/2013/sfi-dynComm/Infomap-0.15.1/results'

	fname_prefix = '{}'.format(type_to_name[comm_type])

	fname = '{}/{}.map'.format(dir_prefix, fname_prefix)

	with open(fname) as ofile:
		line = ofile.readline()

		while line.split(' ')[0] != '*Nodes':
			line = ofile.readline()

		line = ofile.readline()

		while line.split(' ')[0] != '*Links':
			# print line.strip('\n')

			comm_field, id_field, weight_field = line.split(' ')

			comm = int(comm_field.split(':')[0])

			id_lookup = int(id_field.lstrip('\"').rstrip('\"'))

			if comm in comms_to_users:
				comms_to_users[comm].append(lookup_to_userid[id_lookup])
			else:
				comms_to_users[comm] = [lookup_to_userid[id_lookup]]

			line = ofile.readline()

	sizes_comms = [0 for comm in comms_to_users]

	for comm in comms_to_users:
		sizes_comms[comm - 1] = len(comms_to_users[comm])

	comms_ordered = numpy.argsort(sizes_comms)[::-1] + 1

	with open('/Users/daviddarmon/Documents/Reference/R/Research/2013/sfi-dynComm/data/coverings/communities{}i_comp.txt'.format(comm_type), 'w') as wfile:
		for rank in comms_ordered:
			for userid in comms_to_users[rank]:
				wfile.write('{} '.format(userid))

			wfile.write('\n')

	with open('/Users/daviddarmon/Documents/Reference/R/Research/2013/sfi-dynComm/data/coverings/communities{}i_comp_sizes.txt'.format(comm_type), 'w') as wfile:
		for rank in comms_ordered:
			wfile.write('{}\n'.format(len(comms_to_users[rank])))