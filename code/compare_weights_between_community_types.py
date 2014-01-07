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

#	DMD, 311213-18-25

from itertools import islice

# The community type used to determine the
# weights on edges.

# weight_type = 'TE4'
# weight_type = 'hashtag'
weight_type = 'mention-retweet'

if 'TE' in weight_type:
	lag = weight_type.split('E')[1]
	weight_file = '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_{}_withMMBIAS.dat'.format(lag)
elif weight_type == 'hashtag':
	weight_file = '../data/content-full/twitter_network_hashtags_weighted.txt'
elif weight_type == 'mention-retweet':
	weight_file = '../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt'

# The community type used to determine the
# community memberships.

# label_type = 'struc'
# label_type = 'TE4'
# label_type = 'hashtag'
label_type = 'mention-retweet'

if label_type == 'struc':
	label_file  = 'twitter_unweighted_network.txt_oslo_files'
elif 'TE' in label_type:
	lag = label_type.split('E')[1]
	label_file  = 'edge_weights_bin10minutes_lag_{}_withMMBIAS_edgelist.dat_oslo_files'.format(lag)
elif label_type == 'hashtag':
	label_file  = 'twitter_network_hashtags_weighted.txt_oslo_files'
elif label_type == 'mention-retweet':
	label_file  = 'twitter_network_contentfull_weighted_arithmeticmean.txt_oslo_files'

# Generate a dictionary of the form
# {user_id : community_id} from the 
# communities based on the labels.

full_name = '../oslom_outputs/{}/tp'.format(label_file)

comm_dict = {}
comm_count = 0

with open(full_name) as ofile:
	line = ofile.readline()

	while line != '':
		nodes = ofile.readline().strip().split(' ')
		
		for node in nodes:
			comm_dict[node.strip()] = comm_count

		comm_count += 1

		line = ofile.readline()

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

# Note that edges of interest come in one of three flavors:
#
#	internal -> internal
#	internal -> external
#	external -> internal
#
# (There is also external -> external, but we don't care
# about that for this question.)

# Thus, for a given community, say 0, we want to collect
# the edge weights for these three types of communities.

# We'll consider the distribution of these types of weights
# across the ten largest communities for each label type.

if label_type == 'struc':
	comm_of_interests = [199, 184, 192, 191, 84, 196, 170, 179, 198, 105]
elif 'TE' in label_type:
	lag = label_type[-1]

	if lag == '1':
		comm_of_interests = [98, 95, 97, 100, 88, 78, 87, 83, 94, 84]
	elif lag == '2':
		comm_of_interests = [74, 95, 91, 81, 49, 48, 58, 96, 87, 92]
	elif lag == '3':
		comm_of_interests = [97, 99, 104, 96, 91, 76, 71, 95, 79, 84]
	elif lag == '4':
		comm_of_interests = [101, 89, 94, 85, 104, 91, 75, 102, 86, 57]
	elif lag == '5':
		comm_of_interests = [98, 85, 100, 101, 106, 91, 102, 92, 49, 103]
	elif lag == '6':
		comm_of_interests = [103, 104, 105, 96, 73, 98, 85, 92, 77, 67]
elif label_type == 'hashtag':
	comm_of_interests = [274, 232, 275, 278, 250, 262, 288, 253, 264, 270]
elif label_type == 'mention-retweet':
	comm_of_interests = [240, 242, 251, 207, 241, 210, 234, 191, 246, 212]


# Traverse the weighted network (based on the community type)
# and record the types of edges.

if 'TE' in label_type:
	lag = label_type.split('E')[1]
	full_name = '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_{}_withMMBIAS.dat'.format(lag)
elif label_type == 'hashtag':
	full_name = '../data/content-full/twitter_network_hashtags_weighted.txt'
elif label_type == 'mention-retweet':
	full_name = '../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt'
elif label_type == 'struc': # Use the Transfer Entropy file, since it weights all of the links.
	full_name = '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_1_withMMBIAS.dat'

for comm_rank, comm_of_interest in enumerate(comm_of_interests):
	i_to_i = []
	i_to_e = []
	e_to_i = [] 

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
			else:
				if comm_dict[from_id] != comm_of_interest:
					if comm_dict[to_id] != comm_of_interest:
						# print 'external->external'
						pass
					else:
						# print 'external->internal'
						e_to_i.append(weight)
				else:
					if comm_dict[to_id] != comm_of_interest:
						# print 'internal->external'
						i_to_e.append(weight)
					else:
						# print 'internal->internal'
						i_to_i.append(weight)

	print 'There are {} i to i links, {} i to e links, and {} e to i links.'.format(len(i_to_i), len(i_to_e), len(e_to_i))

	output_prefix = 'comm{}_labels-{}_weights-{}'.format(comm_rank, label_type, weight_type)

	with open('../data/edges-by-type/{}_i-to-i.dat'.format(output_prefix), 'w') as wfile:
		for weight in i_to_i:
			wfile.write('{}\n'.format(weight))

	with open('../data/edges-by-type/{}_e-to-i.dat'.format(output_prefix), 'w') as wfile:
		for weight in e_to_i:
			wfile.write('{}\n'.format(weight))

	with open('../data/edges-by-type/{}_i-to-e.dat'.format(output_prefix), 'w') as wfile:
		for weight in i_to_e:
			wfile.write('{}\n'.format(weight))