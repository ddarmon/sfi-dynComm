# Compare how often a mention / retweet occurs
# inter vs intra community, based on the community
# partitioning.

# 	DMD, 13 May 2014

# Outline:

# 1: Extract the userids of the users in the 
# 	 mention-retweet network.
#
# 2: For each network type, determine whether
#    an edge occurs inter- / intra-community.
#
# 3: For each retweet (mention) *made between users 
# 	 from the mention-retweet network*, determine
# 	 whether the retweet (mention) occurs internal
# 	 / external to a community.
#
# UPDATE (26 June 2014): Now we compute this in a
# different way that doesn't positively bias
# coverings with large communities.

from itertools import islice
from collections import Counter

import ipdb

# community_type = '0'

community_types = ['0', '4', '7', '10']
# community_types = ['0', '4', '10']
# community_types = ['4', '7', '10']
# community_types = ['0']

suffix = '' # For OSLOM
# suffix = 'WSBM_K4' # For WSBM

time_frame = '' # For communities inferred using the entire data set
# time_frame = '-partial' # For communities inferred using only the first 3/4 of the data set.

# data_type = 'mentions'
data_type = 'retweets'

print 'Counting {}...'.format(data_type)

# The training set runs 
#
# 	2011/4/25 9am to 2011/5/23 9am.
# 
# which is 28 days or 2419200 seconds.

seconds_train = 2419200

user_files = {'0' : '../data/twitter_network_filtered_edges.txt', '4' : '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_4_withMMBIAS.dat', '7' : '../data/content-full/twitter_network_hashtags_weighted.txt', '10' : '../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt'}

# user_files = {'4' : '../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_4_withMMBIAS.dat', '7' : '../data/content-full/twitter_network_hashtags_weighted.txt', '10' : '../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt'}

# 2: For each network type, determine whether
#    an edge occurs inter- / intra-community.

for community_type_ind, community_type in enumerate(['{}{}'.format(community_type, suffix) for community_type in community_types]):
	# 1: Extract the userids of the users in the 
# 	 various types of networks.
	
	internal_counts_by_community = Counter()
	
	user_present = {}

	user_file = user_files[community_types[community_type_ind]]

	with open(user_file) as ofile:
		if community_types[community_type_ind] == '0':
			for line in ofile:
				uid1, uid2 = line.strip().split('\t')

				user_present[uid1] = True
				user_present[uid2] = True
		elif community_types[community_type_ind] == '4':
			for line in islice(ofile, 1, None):
				uid1, uid2, weight1, weight2 = line.strip().split(',')

				user_present[uid1] = True
				user_present[uid2] = True
		else:
			for line in ofile:
				uid1, uid2, weight = line.strip().split(' ')

				user_present[uid1] = True
				user_present[uid2] = True


	if 'i' in community_type or 'WSBM' in community_type:
		partition_or_covering = 'partition'
	else:
		partition_or_covering = 'covering'

	community_file = '../data/coverings/communities{}{}_comp.txt'.format(community_type, time_frame)

	userid_to_community = {}

	cur_comm = 0

	if partition_or_covering == 'partition':
		with open(community_file) as ofile:
			for line in ofile:
				users = line.strip().split(' ')

				for user in users:
					userid_to_community[user] = cur_comm


				cur_comm += 1
	else:
		with open(community_file) as ofile:
			for line in ofile:
				users = line.strip().split(' ')

				for user in users:
					if user in userid_to_community:
						userid_to_community[user].append(cur_comm)
					else:
						userid_to_community[user] = [cur_comm]


				cur_comm += 1

	# 3: For each retweet (mention) *made between users 
	# 	 from the mention-retweet network*, determine
	# 	 whether the retweet (mention) occurs internal
	# 	 / external to a community.

	tweets_file = '../data/content-full/retweets-mentions/{}2011_userid_zeroed.tsv'.format(data_type)

	if partition_or_covering == 'partition': # If we consider a partition of the nodes, as with the WSBM.
		internal_count = 0 # The number of conversations that occur internal to communities
		external_count = 0 # The number of conversations that occur between communities
		total_count    = 0 # The total number of conversations.
		subset_count   = 0 # The total number of conversations involving those users present in the network-of-interest.

		with open(tweets_file) as ofile:
			for line in islice(ofile, 1, None):
				time, uid1, uid2 = line.strip().split('\t')
				
				time = int(time)

				if time > int(seconds_train): # Only compute the count on the testing data.
					if user_present.get(uid1, False) and user_present.get(uid2, False):
						subset_count += 1 # Count over those users in the network-of-interest

						if userid_to_community[uid1] == userid_to_community[uid2]:
							internal_count += 1
							
							internal_counts_by_community[userid_to_community[uid1]] += 1
						else:
							external_count += 1

					total_count += 1
				else:
					pass
	else: # If we consider a covering of the nodes, as in OSLOM.
		internal_count = 0
		external_count = 0
		subset_count   = 0
		total_count    = 0
		
		already_warned = {}

		with open(tweets_file) as ofile:
			for line in islice(ofile, 1, None):
				time, uid1, uid2 = map(str.strip, line.strip().split('\t'))
				
				time = int(time)
				
				if time > seconds_train: # Only compute the count on the testing data.
					if user_present.get(uid1, False) and user_present.get(uid2, False):
						if len(userid_to_community.get(uid1, [])) == 0:
							if uid1 in already_warned:
								pass
							else:
								print 'Missing user {}'.format(uid1)
								already_warned[uid1] = True
						elif len(userid_to_community.get(uid2, [])) == 0:
							if uid2 in already_warned:
								pass
							else:
								print 'Missing user {}'.format(uid2)
								already_warned[uid2] = True
						else:
							subset_count += 1
							
							# The shared communities between the two users engaged
							# in conversation.
							
							shared_communities = set(userid_to_community[uid1]).intersection(userid_to_community[uid2])
							
							if len(shared_communities) > 0:
								internal_count += 1
								
								for shared_community in shared_communities:
									internal_counts_by_community[shared_community] += 1
							else:
								external_count += 1

					total_count += 1
				else:
					pass

	print 'comm_type\tinternal_count\texternal_count\tsubset_count\t total_count'

	print '{}\t{}\t{}\t{}\t{}'.format(community_type, internal_count, external_count, subset_count, total_count)
	
	# Get out the sizes of the communities.
	
	community_to_size = {}
	
	with open('../data/coverings/communities{}{}_comp_sizes.txt'.format(community_type, time_frame)) as ofile:
		for comm_ind, line in enumerate(ofile):
			community_to_size[comm_ind] = int(line)
	
	mysum = 0
	
	for community_id in internal_counts_by_community.keys():
		mysum += internal_counts_by_community[community_id]/float(community_to_size[community_id])
	
	print 'The score for this community is {}...'.format(mysum/float(subset_count))
	print 'The score for this community is {}...'.format(mysum/float(internal_count))