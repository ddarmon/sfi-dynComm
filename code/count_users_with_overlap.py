# A script to count the number of users
# who belong to more than one community,
# by community-type.
#
#	DMD, 130114-10-28

from collections import Counter

comm_types = [0, 4, 7, 10]

community_labels = {0 : 'structural', 4 : 'behavior', 7 : 'topic', 10 : 'activity'}

with open('tmp.dat', 'w') as wfile:
	for comm_type in comm_types:
		label_file = 'mutual3/coverings/no_singletons/communitites{}_comp.txt'.format(comm_type)

		# A dictionary of the form
		# 	{userid : num_communities}

		user_dict = Counter()
		overlap_dict = Counter()

		with open(label_file) as ofile:
			for comm_id, line in enumerate(ofile):
				nodes = line.strip().split(' ')

				for node in nodes:
					user_dict[node] += 1

		num_nodes_with_overlap = 0

		for node in user_dict:
			if user_dict[node] > 1:
				overlap_dict[user_dict[node]] += 1
				num_nodes_with_overlap += 1
				# print node, user_dict[node]

		print label_file, num_nodes_with_overlap, overlap_dict

		# to_print = '{} '.format(community_labels[comm_type])

		for ind in range(2, 5):
			# print '{} {} {}'.format(community_labels[comm_type], ind, overlap_dict[ind])

			# to_print += '{} '.format(overlap_dict[ind])
			for cur_ind in range(overlap_dict[ind]):
				wfile.write('{} {}\n'.format(community_labels[comm_type], ind))