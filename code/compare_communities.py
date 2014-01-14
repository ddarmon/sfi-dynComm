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
		#hashtags_vector[user].append((tfidf,h))
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

for c in hashtag_communities_users:
	#hashtags = {}
	#for u in hashtag_communities_users[c]:
	#	#if c == '114': print u,hashtags_vector[u]
	#	hashtags[u] = set()
	#	for (score,h) in hashtags_vector[u]:
	#		hashtags[u].add(h)
	#hashtags_intersection = set.intersection(*hashtags.values())
	#print c,hashtag_communities_size[c],hashtag_communities_bs[c],hashtags_intersection
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
	print c,hashtag_communities_size[c],hashtag_communities_bs[c]
	for n in sorted(nb_hashtags.keys(),reverse=True):
		if hashtag_communities_size[c] > 2:
			if n > hashtag_communities_size[c]/3: print n,nb_hashtags[n]
		else:
			if n == hashtag_communities_size[c]: print n,nb_hashtags[n] 






