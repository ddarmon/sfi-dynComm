#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import igraph
import math

def integers_distribution(input_vector,string):
	outfile = open(string+'_distribution.txt','w')
	xmax = max(input_vector)
	hist_vector_temp = []
	for i in range(xmax+1):
		hist_vector_temp.append(0)
	for i in input_vector:
		hist_vector_temp[i] += 1
	for i in range(len(hist_vector_temp)):
		if hist_vector_temp[i] != 0:
			outfile.write('%d\t%d\n'%(i,hist_vector_temp[i]))
	outfile.close()

isuser = 0
isfollower = 0

infile = open('data/_follower_15K_user.txt/_follower_15K_user.txt','r')
lines = infile.readlines()
nodes = set(); edges = []; neighbors = {}
for line in lines:
	row = line.split()
	user = row[0]
	follower = row[2]
	nodes.add(user); nodes.add(follower)
	edges.append((user,follower))
#	if user == '51319087':
#		isuser += 1
#	if follower == '51319087':
#		isfollower += 1
	if user in neighbors: neighbors[user].append(follower)
	else: neighbors[user] = [follower]
infile.close()
print 'number of nodes:',len(nodes)
print 'number of edges:',len(edges)

#print isuser,isfollower

edges_weights = {}
retweet_edges_weights = {}
mentions_edges_weights = {}

#hasretweeted = 0
#wasretweeted = 0
#hasmentioned = 0
#wasmentioned = 0

infile = open('data/retweets-mentions/retweets2011_userid.tsv','r')
lines = infile.readlines()
user_hasretweeted = {}
for u in nodes: user_hasretweeted[u] = 0
user_wasretweeted = {}
for u in nodes: user_wasretweeted[u] = 0
retweets_nodes = set()
nb_retweets = 0
for line in lines:
	row = line.split('\t')	
	u1 = row[1]
	u2 = row[2][:-1]
	retweets_nodes.add(u1)
	retweets_nodes.add(u2)
#	if u1 == '51319087':
#		hasretweeted += 1
#	if u2 == '51319087':
#		wasretweeted += 1
	if u1 in nodes and u2 in nodes:
		nb_retweets += 1
		user_hasretweeted[u1] += 1
		user_wasretweeted[u2] += 1
		if (u2,u1) in edges_weights: edges_weights[(u2,u1)] += 1
		else: edges_weights[(u2,u1)] = 1
		if (u2,u1) in retweet_edges_weights: retweet_edges_weights[(u2,u1)] += 1
		else: retweet_edges_weights[(u2,u1)] = 1
infile.close()

infile = open('data/retweets-mentions/mentions2011_userid.tsv','r')
lines = infile.readlines()
user_hasmentioned = {}
for u in nodes: user_hasmentioned[u] = 0
user_wasmentioned = {}
for u in nodes: user_wasmentioned[u] = 0
mentions_nodes = set()
nb_mentions = 0
for line in lines:
	row = line.split('\t')
	u1 = row[1]
	u2 = row[2][:-1]
	mentions_nodes.add(u1)
	mentions_nodes.add(u2)
#	if u1 == '51319087':
#		hasmentioned += 1
#	if u2 == '51319087':
#		wasmentioned += 1
	if u1 in nodes and u2 in nodes:
		nb_mentions += 1
		user_hasmentioned[u1] += 1
		user_wasmentioned[u2] += 1
		if (u1,u2) in edges_weights: edges_weights[(u1,u2)] += 1
		else: edges_weights[(u1,u2)] = 1
		if (u1,u2) in mentions_edges_weights: mentions_edges_weights[(u1,u2)] += 1
		else: mentions_edges_weights[(u1,u2)] = 1
infile.close()

#print nb_retweets,nb_mentions

#print hasretweeted, wasretweeted, hasmentioned, wasmentioned

#print len(nodes)
#print len(retweets_nodes)
#print len(mentions_nodes)
#retweets_nodes.issubset(nodes)
#mentions_nodes.issubset(nodes)

print 'min and max number of retweets made:',min(user_hasretweeted.values()),max(user_hasretweeted.values())
print 'min and max number of retweets received:',min(user_wasretweeted.values()),max(user_wasretweeted.values())
print 'min and max number of mentions made:',min(user_hasmentioned.values()),max(user_hasmentioned.values())
print 'min and max number of mentions received:',min(user_wasmentioned.values()),max(user_wasmentioned.values())

integers_distribution(user_hasretweeted.values(),'retweets_made')
integers_distribution(user_wasretweeted.values(),'retweets_received')
integers_distribution(user_hasmentioned.values(),'mentions_made')
integers_distribution(user_wasmentioned.values(),'mentions_received')

filtered_nodes_temporary = set()
incoming_info_vector = []; outgoing_info_vector = []
for u in nodes:
	incoming_info = user_hasretweeted[u]+user_wasmentioned[u]
	outgoing_info = user_wasretweeted[u]+user_hasmentioned[u]
	incoming_info_vector.append(incoming_info)
	outgoing_info_vector.append(outgoing_info)
	if incoming_info > 8 and outgoing_info > 8:
		filtered_nodes_temporary.add(u)
print 'number of nodes:',len(filtered_nodes_temporary)

t = 8
#outfile = open('threshold_swap.txt','w')
#thresholds = []
#for i in range(631): thresholds.append(i)
#for i in range(len(thresholds)):
#	if i % 100 == 0: print i
#	t = thresholds[i]
user_nbtweets = {}
filtered_nodes = set()
for u in nodes:#filtered_nodes_temporary:
	try:
		tweet_history_file = open('data/tweet_times_2011/tweet_times_'+u+'.dat','r')
		tweet_history_lines = tweet_history_file.readlines()
		nb_tweets = len(tweet_history_lines)
		user_nbtweets[u] = nb_tweets
		if u in filtered_nodes_temporary and nb_tweets > t:
			filtered_nodes.add(u)
	except:
		pass
print 'number of nodes:',len(filtered_nodes)
filtered_edges = []
for n1 in filtered_nodes:
	if n1 in neighbors:
		for n2 in set(neighbors[n1]).intersection(filtered_nodes):
			filtered_edges.append((n1,n2))
print 'number of edges:',len(filtered_edges)

integers_distribution(incoming_info_vector,'incoming_info')
integers_distribution(outgoing_info_vector,'outgoing_info')

integers_distribution(user_nbtweets.values(),'nb_tweets')

g = igraph.Graph(directed=True)
g.add_vertices(list(filtered_nodes))
g.add_edges(filtered_edges)
components = g.clusters()
#sizes = []
maxsize = 0
for c in components:
	if len(c) > maxsize:
		maxsize = len(c)
		giant_component = c
	#sizes.append(len(c))
print 'giant connected component size:',maxsize
#print sizes

final_edge_list = []
final_weights_list = []
arit_final_weights_list = []
arit_final_edge_list = []

retweets_edge_list = []
retweets_weights_list = []
mentions_edge_list = []
mentions_weights_list = []

nb_edges = 0
checkind = 0
giant_components_nodes = []
contentfree_edge_list = []
outfile = open('twitter_network_filtered.txt','w')
outfile.write('#nodes (user ids)\n')
outfile1 = open('twitter_network_filtered_nodes.txt','w')
outfile2 = open('twitter_network_filtered_edges.txt','w')
for i in giant_component:
	outfile.write('%s\n' % g.vs[i]['name'])
	outfile1.write('%s\n' % g.vs[i]['name'])
	giant_components_nodes.append(g.vs[i]['name'])
outfile.write('#edges\n')
for i in giant_component:
	n1 = g.vs[i]['name']
	for n2 in set(neighbors[n1]).intersection(giant_components_nodes):
		outfile.write('%s\t%s\n'%(n1,n2))
		outfile2.write('%s\t%s\n'%(n1,n2))
		nb_edges += 1
		contentfree_edge_list.append((n1,n2))
		if (n1,n2) in retweet_edges_weights: 
			w1 = float(retweet_edges_weights[(n1,n2)]) / float(user_hasretweeted[n2])
			retweets_edge_list.append((n1,n2))
			retweets_weights_list.append(w1)
		else: w1 = 0.0
		if (n1,n2) in mentions_edges_weights: 
			w2 = float(mentions_edges_weights[(n1,n2)]) / float(user_wasmentioned[n2])
			mentions_edge_list.append((n1,n2))
			mentions_weights_list.append(w2)
		else: w2 = 0.0
		if w1+w2 > 0:
			w = 2*w1*w2/(w1+w2)
			arit_w = 0.5*(w1+w2)
			if w > 0:
				final_weights_list.append(w)
				final_edge_list.append((n1,n2))
			if arit_w > 0:
				arit_final_weights_list.append(arit_w)
				arit_final_edge_list.append((n1,n2))
outfile.close()
outfile1.close()
outfile2.close()

retweets_network = igraph.Graph(directed=True)
retweets_network.add_vertices(giant_components_nodes)
retweets_network.add_edges(retweets_edge_list)
retweets_network.es['weight'] = retweets_weights_list
retweets_network.write_ncol('twitter_network_retweets.txt')

mentions_network = igraph.Graph(directed=True)
mentions_network.add_vertices(giant_components_nodes)
mentions_network.add_edges(mentions_edge_list)
mentions_network.es['weight'] = mentions_weights_list
mentions_network.write_ncol('twitter_network_mentions.txt')

network = igraph.Graph(directed=True)
network.add_vertices(giant_components_nodes)
network.add_edges(final_edge_list)
network.es['weight'] = final_weights_list
#network.write_pajek('twitter_network_contentfull_weighted.net')
network.write_ncol('twitter_network_contentfull_weighted_harmonicmean.txt')

arit_network = igraph.Graph(directed=True)
arit_network.add_vertices(giant_components_nodes)
arit_network.add_edges(arit_final_edge_list)
arit_network.es['weight'] = arit_final_weights_list
arit_network.write_ncol('twitter_network_contentfull_weighted_arithmeticmean.txt')

g = igraph.Graph(directed=True)
g.add_vertices(giant_components_nodes)
g.add_edges(contentfree_edge_list)
g.write_ncol('twitter_unweighted_network.txt')
integers_distribution(g.degree(mode='OUT'),'out_degree')
integers_distribution(g.degree(mode='IN'),'in_degree')

print 'binary network:',len(g.vs),'nodes &',len(g.es),'edges'
print 'retweets and mentions weighted network:',len(network.vs),'nodes &',len(network.es),'edges'

# hashtags weighted network

user_hashtags = {}; hashtag_users = {}; hashtags = set()
infile = open('data/hashtags_2011/hashtags_2011.tsv','r')
lines = infile.readlines()
for line in lines[1:]:
	row = line.split('\t')
	user = row[0]
	if user in giant_components_nodes:
		tweet = row[2][:-1]
		words = tweet.split()
		for w in words:
			if w[0] == '#':	
				h = w.lower()
				if user in user_hashtags: user_hashtags[user].append(h)
				else: user_hashtags[user] = [h]
				if h in hashtag_users: hashtag_users[h].add(user)
				else: hashtag_users[h] = set([user])
				hashtags.add(h)

nb_hasthtags = []
for u in user_hashtags:
	nb_hasthtags.append(len(set(sorted(user_hashtags[u]))))
integers_distribution(nb_hasthtags,'nb_hashtags')

#user_hashtags = {'u1':['h1','h2','h2','h3'],'u2':['h2','h4']}; hashtag_users = {'h1':set(['u1']),'h2':set(['u1','u2']),'h3':set(['u1']),'h4':set(['u2'])}
print 'number of hashtags:',len(hashtags)

outfile = open('users_hashtags.txt','w')
nb_users = len(user_hashtags)
print 'nb users using hashtags:',nb_users
tfidf = {}; norm_tfidf = {}
for u in user_hashtags:
	outfile.write('%s;'%u)
	tfidf[u] = {}
	norm_tfidf[u] = 0.0
	for h in user_hashtags[u]:
		f = user_hashtags[u].count(h)
		nb_users_h = len(hashtag_users[h])
		tfidf[u][h] = f * math.log( float(nb_users) / float(nb_users_h) )
		norm_tfidf[u] += ( tfidf[u][h] * tfidf[u][h] )
	norm_tfidf[u] = math.sqrt(norm_tfidf[u])
	for h in tfidf[u]:
		outfile.write('%s %f\t'%(h,tfidf[u][h]))
	outfile.write('\n')
outfile.close()

hashtags_edges = {}; hashtags_nodes = set()
i = 0
for u1 in g.vs["name"]:
	if i % 500 == 0: print i,'over',len(g.vs["name"])
	if u1 in user_hashtags:
		for j in g.neighbors(u1,mode='OUT'):
			u2 = g.vs[j]["name"]
			if u2 in user_hashtags:
				common_hashtags = set(user_hashtags[u1]).intersection(set(user_hashtags[u2]))
				if len(common_hashtags) > 0:
					w = 0
					for h in common_hashtags:
						w += ( tfidf[u1][h] * tfidf[u2][h] )
					w = float(w) / float( norm_tfidf[u1] * norm_tfidf[u2] )
					hashtags_edges[(u1,u2)] = w
					hashtags_nodes.add(u1)
					hashtags_nodes.add(u2)
	i += 1

hashtags_network = igraph.Graph(directed=True)
hashtags_network.add_vertices(list(hashtags_nodes))
hashtags_network.add_edges(hashtags_edges.keys())
hashtags_network.es['weight'] = hashtags_edges.values()
hashtags_network.write_ncol('twitter_network_hashtags_weighted.txt')

print 'hashtags weighted network:',len(hashtags_network.vs),'nodes &',len(hashtags_network.es),'edges'
