#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

hashtags_file = open('../data/users_hashtags.txt','r')
hashtags_vector = {}
lines = hashtags_file.readlines()
for line in lines:
	row = line.split(';')
	user = row[0]
	hashtags_vector[user] = []
	elements = row[1][:-1].split('\t')
	for element in elements[:-1]:
		h = element.split()[0]
		tfidf = float(element.split()[1])
		hashtags_vector[user].append(h)

hashtags_communities_file = open('../oslom_outputs/twitter_network_hashtags_weighted.txt_oslo_files/tp_without_singletons','r')
hashtag_communities_size = {}; hashtag_communities_bs = {}; hashtag_communities_users = {}
lines = hashtags_communities_file.readlines()
for i in range(len(lines)):
	if i % 2 == 0:
		line = lines[i].split()
		module = line[1]
		size =  int(line[3])
		bs = float(line[5])
		hashtag_communities_size[module] = size
		hashtag_communities_bs[module] = bs
		users = lines[i+1].split()
		hashtag_communities_users[module] = users

retweets_communities_file = open('../oslom_outputs/twitter_network_retweets.txt_oslo_files/tp_without_singletons','r')
retweets_communities_size = {}; retweets_communities_bs = {}; retweets_communities_users = {}
lines = retweets_communities_file.readlines()
for i in range(len(lines)):
	if i % 2 == 0:
		line = lines[i].split()
		module = line[1]
		size =  int(line[3])
		bs = float(line[5])
		retweets_communities_size[module] = size
		retweets_communities_bs[module] = bs
		users = lines[i+1].split()
		retweets_communities_users[module] = users

mentions_communities_file = open('../oslom_outputs/twitter_network_mentions.txt_oslo_files/tp_without_singletons','r')
mentions_communities_size = {}; mentions_communities_bs = {}; mentions_communities_users = {}
lines = mentions_communities_file.readlines()
for i in range(len(lines)):
	if i % 2 == 0:
		line = lines[i].split()
		module = line[1]
		size =  int(line[3])
		bs = float(line[5])
		mentions_communities_size[module] = size
		mentions_communities_bs[module] = bs
		users = lines[i+1].split()
		mentions_communities_users[module] = users

contentfull_communities_file = open('../oslom_outputs/twitter_network_contentfull_weighted_arithmeticmean.txt_oslo_files/tp_without_singletons','r')
contentfull_communities_size = {}; contentfull_communities_bs = {}; contentfull_communities_users = {}
lines = contentfull_communities_file.readlines()
for i in range(len(lines)):
	if i % 2 == 0:
		line = lines[i].split()
		module = line[1]
		size =  int(line[3])
		bs = float(line[5])
		contentfull_communities_size[module] = size
		contentfull_communities_bs[module] = bs
		users = lines[i+1].split()
		contentfull_communities_users[module] = users

te4_communities_file = open('../oslom_outputs/edge_weights_bin10minutes_lag_4_withMMBIAS_edgelist.dat_oslo_files/tp_without_singletons','r')
te4_communities_size = {}; te4_communities_bs = {}; te4_communities_users = {}
lines = te4_communities_file.readlines()
for i in range(len(lines)):
	if i % 2 == 0:
		line = lines[i].split()
		module = line[1]
		size =  int(line[3])
		bs = float(line[5])
		te4_communities_size[module] = size
		te4_communities_bs[module] = bs
		users = lines[i+1].split()
		te4_communities_users[module] = users


for c in hashtag_communities_users:
	hashtags = set()
	hashtag_nbusers = {}
	for u in hashtag_communities_users[c]:
		for h in hashtags_vector[u]: 
			hashtags.add(h)
			if h in hashtag_nbusers: hashtag_nbusers[h] += 1
			else: hashtag_nbusers[h] = 1
	nb_hashtags = {}
	for h in hashtag_nbusers:
		n = hashtag_nbusers[h]
		if n in nb_hashtags: nb_hashtags[n].append(h)
		else: nb_hashtags[n] = [h]

	retweets_fractions = []
	for c2 in retweets_communities_users:
		comm_intersection = set(hashtag_communities_users[c]) & set(retweets_communities_users[c2])
		if len(comm_intersection) > 1:
			retweets_fractions.append(float(len(comm_intersection))/float(len(hashtag_communities_users[c])))

	mentions_fractions = []
	for c2 in mentions_communities_users:
		comm_intersection = set(hashtag_communities_users[c]) & set(mentions_communities_users[c2])
		if len(comm_intersection) > 1:
			mentions_fractions.append(float(len(comm_intersection))/float(len(hashtag_communities_users[c])))

	contentfull_fractions = []
	for c2 in contentfull_communities_users:
		comm_intersection = set(hashtag_communities_users[c]) & set(contentfull_communities_users[c2])
		if len(comm_intersection) > 1:
			contentfull_fractions.append(float(len(comm_intersection))/float(len(hashtag_communities_users[c])))

	te4_fractions = []
	for c2 in te4_communities_users:
		comm_intersection = set(hashtag_communities_users[c]) & set(te4_communities_users[c2])
		if len(comm_intersection) > 1:
			te4_fractions.append(float(len(comm_intersection))/float(len(hashtag_communities_users[c])))

	if hashtag_communities_size[c] > 9:
		outfile = open('community_inspection/size_'+str(hashtag_communities_size[c])+'_module_'+c+'.txt','w')
		outfile.write('#module %s\tsize %d\tbs %f\n'%(c,hashtag_communities_size[c],hashtag_communities_bs[c]))
		for n in sorted(nb_hashtags.keys(),reverse=True): 
			if float(n)/float(hashtag_communities_size[c]) > 0.3: outfile.write('%d\t%s\n'%(n,list(nb_hashtags[n])))
		outfile.write('retweets communities\t%s\n'%sorted(retweets_fractions,reverse=True))
		outfile.write('mentions communities\t%s\n'%sorted(mentions_fractions,reverse=True))
		outfile.write('contentfull communities\t%s\n'%sorted(contentfull_fractions,reverse=True))
		outfile.write('te4 communities\t%s\n'%sorted(te4_fractions,reverse=True))






