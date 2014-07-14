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
# UPDATE (2 July 2014): This implementation uses
# Elisa's conversation tracking idea from the 
# 1 July 2014 email.
# 
# UPDATE (3 July 2014): Tracking both mentions
# and retweets simulataneously as 'conversations'.

from itertools import islice
from collections import Counter

import ipdb

# community_type = '0'

# community_types = ['0', '4', '7', '10']
# community_types = ['0', '4', '10']
# community_types = ['4', '7', '10']
community_types = ['10']

# community_types = ['10']

suffix = '' # For OSLOM
# suffix = 'WSBM_K4' # For WSBM

# time_frame = '' # For communities inferred using the entire data set
time_frame = '-partial' # For communities inferred using only the first 1/2 of the data set.

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
	external_counts_by_community = Counter()
	
	i_edge_counts_by_community = Counter() # Count the number of edges *internal* to a community
	e_edge_counts_by_community = Counter() # Count the number of edges *incoming* to / *outgoing* from a community
	
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
	
	# Get out the number of internal edges for each community
	# and the number of external edges for each community,
	# both going into and going out of the community.
	
	with open(user_file) as ofile:
		if community_types[community_type_ind] == '4':
			num_skip = 1
		else:
			num_skip = 0
		
		for line in islice(ofile, num_skip, None):
			if community_types[community_type_ind] == '0':
				uid1, uid2 = line.strip().split('\t')
			elif community_types[community_type_ind] == '4':
				uid1, uid2, weight1, weight2 = map(str.strip, line.strip().split(','))
			else:
				uid1, uid2, weight = map(str.strip, line.strip().split(' '))
			
			if len(userid_to_community.get(uid1, [])) == 0:
				pass
			elif len(userid_to_community.get(uid2, [])) == 0:
				pass
			else:
			# if uid1 == '51319087':
			# 	pass
			# elif uid2 == '51319087':
			# 	pass
			# else:
				# The shared communities between the two users engaged
				# in conversation.
				
				shared_communities = set(userid_to_community[uid1]).intersection(userid_to_community[uid2])
			
				if len(shared_communities) > 0:
					for shared_community in shared_communities:
						i_edge_counts_by_community[shared_community] += 1
				else:
					for commid in userid_to_community[uid1]:
						e_edge_counts_by_community[commid] += 1
					for commid in userid_to_community[uid2]:
						e_edge_counts_by_community[commid] += 1
	
	# Get out the number of communities.
	
	comm_count = 0
	
	with open('../data/coverings/communities{}{}_comp_sizes.txt'.format(community_type, time_frame)) as ofile:
		for comm_ind, line in enumerate(ofile):
			comm_count += 1

	# 3: For each retweet + mention *made between users 
	# 	 from the mention-retweet network*, determine
	# 	 whether the retweet + mention occurs internal
	# 	 / external to a community.
	
	for data_type in ['mentions', 'retweets']:
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
							
								external_counts_by_community[userid_to_community[uid1]] += 1
								external_counts_by_community[userid_to_community[uid2]] += 1

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
								if uid1 == uid2: # Sometimes the users mention *themselves*
									pass
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
										for commid in userid_to_community[uid1]:
											external_counts_by_community[commid] += 1
										for commid in userid_to_community[uid2]:
											external_counts_by_community[commid] += 1

							total_count += 1
					else:
						pass
	
	# Print the results.
	
	print 'comm\ti_convs\te_convs\ti_edges\te_edges\n'

	for commid in range(comm_count):
		print commid, internal_counts_by_community[commid], external_counts_by_community[commid], i_edge_counts_by_community[commid], e_edge_counts_by_community[commid]

	print 'comm\ti_convs\te_convs\ti_edges\te_edges\n'
	
	num_comms_excluded = 0 # The number of total communities excluded
	
	num_wo_ec = 0 # The number of communities where ec = 0, meaning that
				  # *no* conversations occur external to the community.
	
	running_sum = 0 # the sum of the ratios of ic/(ec + 1) across all of the communities
	
	ratios = []
	
	for commid in range(comm_count):
		if i_edge_counts_by_community[commid] == 0 or e_edge_counts_by_community[commid] == 0:
			num_comms_excluded += 1 # Deal with singletons and communities without non-inter-type edges
		else:
			ic = float(internal_counts_by_community[commid])/i_edge_counts_by_community[commid]
			ec = float(external_counts_by_community[commid])/e_edge_counts_by_community[commid]
			
			# print ic, ec
			
			if ec == 0:
				num_wo_ec += 1
			
			ratios.append(ic/float(ec+1))
			
			running_sum += ic/float(ec+1)
			
	
	num_comms_included = comm_count - num_comms_excluded
	
	print 'The conversation quality score for this community type is {}...'.format(running_sum/float(num_comms_included))