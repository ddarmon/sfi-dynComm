# A script to compare the weights for
# edges inside / outside of a community
# where we use a community of type C
# and a weight of type B.
# 
# For example, we might consider the
# communities based on transfer entropy
# and the weights based on hashtags.
# 
# This allows us to narrow in on the 
# characteristics of the community
# types.

#	DMD, 23 April 2014

from itertools import islice
import numpy
import collections

# The community type used to determine the
# weights on edges.

# weight_type = 'TE4'
# weight_type = 'hashtag'
# weight_type = 'mention-retweet'

# The community type used to determine the
# community memberships.

# label_type = 'struc'
# label_type = 'TE4'
# label_type = 'hashtag'
# label_type = 'mention-retweet'

# The community detection algorithm, either 
# '', which corresponds to OSLOM, or 'i',
# which corresponds to InfoMap.

# comm_alg = 'i' # For InfoMap
#
# comm_alg = 'WSBM_K10' # For WSBM

comm_alg = '' # For OSLOM

label_type_to_number = {'struc' : 0, 'TE4' : 4, 'hashtag' : 7, 'mention-retweet' : 10}

for weight_type in ['TE4', 'hashtag', 'mention-retweet']:
	for label_type in ['struc', 'TE4', 'hashtag', 'mention-retweet']:
	# for label_type in ['struc', 'mention-retweet']:
		print 'Working on {}/{} pairing...'.format(weight_type, label_type)

		if 'TE' in weight_type:
			lag = weight_type.split('E')[1]
			weight_file = '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_{}_withMMBIAS.dat'.format(lag)
		elif weight_type == 'hashtag':
			weight_file = '../data/content-full/twitter_network_hashtags_weighted.txt'
		elif weight_type == 'mention-retweet':
			weight_file = '../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt'

		label_file  = '../data/coverings/communities{}{}_comp.txt'.format(label_type_to_number[label_type], comm_alg)

		# Generate a dictionary of the form
		# {user_id : community_id} from the 
		# communities based on the labels.

		comm_dict = collections.defaultdict(set)
		comm_count = 0

		comm_sizes = []

		with open(label_file) as ofile:
			for line in ofile:
				nodes = line.strip().split(' ')

				comm_sizes.append(len(nodes))
				
				if len(nodes) == 1:
					comm_dict[node.strip()] = 's' # Label the singletons as such.
				else:
					for node in nodes:
						comm_dict[node.strip()] = comm_dict[node.strip()].union(set([comm_count]))

				comm_count += 1

		order_comm_sizes = numpy.argsort(numpy.array(comm_sizes))[::-1]

		# Create a dictionary representation of the weighted network
		# that determines the *weights* we'll consider. The 
		# dictionary is of the form
		#
		# 	(from_id, to_id) : weight

		edges = {}

		with open(weight_file) as ofile:
			# The transfer entropy files are csv 
			# with a header, while all of the other files
			# are space separated without a header.

			if 'TE' in weight_type:
				for line in islice(ofile, 1, None):
					from_id, to_id, weight, weight_MM = line.strip().split(',')
					from_id = from_id.strip(); to_id = to_id.strip(); weight = weight.strip(); weight_MM = weight_MM.strip()

					edges[(from_id, to_id)] = float(weight_MM)
			else:
				for line in ofile:
					from_id, to_id, weight = line.strip().split(' ')

					edges[(from_id, to_id)] = float(weight)

		# Note that edges of interest come in one of two flavors:
		#
		#	internal -> internal
		#	internal -> external / external -> internal
		#

		comm_of_interests = order_comm_sizes # Go through the communities, from largest to smallest.

		# Traverse the weighted network (based on the community type)
		# and partition the edges into inter, intra, and multi
		# and record to a file.

		if 'TE' in label_type:
			lag = label_type.split('E')[1]
			full_name = '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_{}_withMMBIAS.dat'.format(lag)
		elif label_type == 'hashtag':
			full_name = '../data/content-full/twitter_network_hashtags_weighted.txt'
		elif label_type == 'mention-retweet':
			full_name = '../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt'
		elif label_type == 'struc': # Use the Transfer Entropy file, since it weights all of the links.
			full_name = '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_1_withMMBIAS.dat'

		inter = []
		intra = []
		multi = []

		with open(full_name) as ofile:
			for line in islice(ofile, 1, None):
				if ',' in line: # The transfer entropy files
					from_id, to_id, weight_biased, weight = line.split(',')
					to_id = to_id.lstrip() # Some of the to_ids have leading white space

				else:
					from_id, to_id, dummy_weight = line.split(' ')

				weight = edges.get((from_id, to_id), 0)

				if weight < 0:
					weight = 0. # To deal with the MM corrector sometimes giving negative biases

				if from_id == '51319087' or to_id == '51319087':
					pass
				elif comm_dict[from_id] == 's' or comm_dict[to_id] == 's': # Ignore singleton edges
					pass
				else:
					# Get out the community memberships of each
					# node incident on the edge. Call these 
					# sets of communities A and B.

					A = comm_dict[from_id]; B = comm_dict[to_id]

					# Compute the intersection between these sets,
					# giving the *shared* memberships.

					I = A.intersection(B)

					if len(I) == 0:
						inter.append(weight)
					# elif len(A) == len(B) and len(A) == len(I):
					elif A == B:
						intra.append(weight)
					else:
						multi.append(weight)

		print 'There are {} inter links, {} intra links, and {} multi links.'.format(len(inter), len(intra), len(multi))

		if comm_alg == '':
			output_prefix = 'interintramulti_labels-{}_weights-{}'.format(label_type, weight_type)
		else:
			output_prefix = 'interintramulti_labels-{}_{}_weights-{}'.format(label_type, comm_alg, weight_type)

		with open('../data/edges-by-type/{}_inter.dat'.format(output_prefix), 'w') as wfile:
			for weight in inter:
				wfile.write('{}\n'.format(weight))

		with open('../data/edges-by-type/{}_intra.dat'.format(output_prefix), 'w') as wfile:
			for weight in intra:
				wfile.write('{}\n'.format(weight))

		with open('../data/edges-by-type/{}_multi.dat'.format(output_prefix), 'w') as wfile:
			for weight in multi:
				wfile.write('{}\n'.format(weight))