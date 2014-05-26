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

from itertools import islice

import ipdb


# 1: Extract the userids of the users in the 
# 	 mention-retweet network.

user_present = {}

user_file = '../data/content-full/twitter_network_contentfull_weighted_arithmeticmean.txt'

with open(user_file) as ofile:
	for line in ofile:
		uid1, uid2, weight = line.strip().split(' ')

		user_present[uid1] = True
		user_present[uid2] = True

# 2: For each network type, determine whether
#    an edge occurs inter- / intra-community.

# community_type = '0'

# community_types = ['0', '4', '10']
community_types = ['0', '10']

suffix = 'WSBM_K5'

for community_type in ['{}{}'.format(community_type, suffix) for community_type in community_types]:

	data_type = 'mentions'
	# data_type = 'retweets'

	if 'i' in community_type or 'WSBM' in community_type:
		partition_or_covering = 'partition'
	else:
		partition_or_covering = 'covering'

	community_file = '../data/coverings/communities{}_comp.txt'.format(community_type)

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

	if partition_or_covering == 'partition':
		internal_count = 0
		external_count = 0
		total_count    = 0

		with open(tweets_file) as ofile:
			for line in islice(ofile, 1, None):
				time, uid1, uid2 = line.strip().split('\t')

				if user_present.get(uid1, False) and user_present.get(uid2, False):
					if userid_to_community[uid1] == userid_to_community[uid2]:
						internal_count += 1
					else:
						external_count += 1

				total_count += 1

		print 'comm_type\tinternal_count\texternal_count\ttotal_count'

		print '{}\t{}\t{}\t{}'.format(community_type, internal_count, external_count, total_count)
	else:
		internal_count = 0
		external_count = 0
		subset_count   = 0
		total_count    = 0

		with open(tweets_file) as ofile:
			for line in islice(ofile, 1, None):
				time, uid1, uid2 = line.strip().split('\t')

				if user_present.get(uid1, False) and user_present.get(uid2, False):
					# if userid_to_community.get(uid1, True):
					# 	print 'Missing user {}'.format(uid1)
					# elif userid_to_community.get(uid2, True):
					# 	print 'Missing user {}'.format(uid2)
					# else:
					subset_count += 1

					if len(set(userid_to_community[uid1]).intersection(userid_to_community[uid2])) > 0:
						internal_count += 1
					else:
						external_count += 1

				total_count += 1

		print 'comm_type\tinternal_count\texternal_count\ttotal_count'

		print '{}\t{}\t{}\t{}'.format(community_type, internal_count, external_count, total_count)