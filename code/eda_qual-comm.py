import webbrowser
import numpy

# The weights used to determine the community 
# labels.

# label_type = 'struc'
# label_type = 'TE4'
# label_type = 'hashtag'
label_type = 'mention-retweet'

print '\nUsing weights of type {}\n'.format(label_type)

if label_type == 'struc':
	label_file  = 'twitter_unweighted_network.txt_oslo_files'
elif 'TE' in label_type:
	lag = label_type.split('E')[1]
	label_file  = 'edge_weights_bin10minutes_lag_{}_withMMBIAS_edgelist.dat_oslo_files'.format(lag)
elif label_type == 'hashtag':
	label_file  = 'twitter_network_hashtags_weighted.txt_oslo_files'
elif label_type == 'mention-retweet':
	label_file  = 'twitter_network_contentfull_weighted_arithmeticmean.txt_oslo_files'

full_name = '../oslom_outputs/{}/tp_without_singletons'.format(label_file)

# Generate a dictionary of the form
# {community_id : [userid1, userid2, ...]}
# from the communities based on the labels.

comm_dict = {}
comm_count = 0

comm_sizes = []

with open(full_name) as ofile:
	line = ofile.readline()

	while line != '':
		nodes = ofile.readline().strip().split(' ')
		
		comm_dict[comm_count] = nodes

		comm_count += 1

		comm_sizes.append(len(nodes))

		line = ofile.readline()


# Get out the ranking, in size, of the communities,
# from smallest to largest.

comm_sorted = numpy.argsort(comm_sizes)

# comm_id = comm_sorted[-1] # Start with the largest community
comm_id = comm_sorted[0] # Start with the smallest community

print 'Community {} using the weight type {} has {} members.'.format(comm_id, label_type, len(comm_dict[comm_id]))

at_a_time = 5 # Open this many at a time.

for ind, node in enumerate(comm_dict[comm_id]):
	webbrowser.open('http://twitter.com/account/redirect_by_id?id={}'.format(node))

	if (ind+1)%at_a_time == 0:
		raw_input("")