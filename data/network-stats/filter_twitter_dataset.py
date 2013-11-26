#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import igraph

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

infile = open('data/_follower_15K_user.txt/_follower_15K_user.txt','r')
lines = infile.readlines()
nodes = set(); edges = []; neighbors = {}
for line in lines:
	row = line.split()
	user = row[0]
	follower = row[2]
	nodes.add(user); nodes.add(follower)
	edges.append((user,follower))
	if user in neighbors: neighbors[user].append(follower)
	else: neighbors[user] = [follower]
print 'number of nodes:',len(nodes)
print 'number of edges:',len(edges)

edges_weights = {}

infile = open('data/retweets-mentions/retweets2011_userid.tsv','r')
lines = infile.readlines()
user_hasretweeted = {}
for u in nodes: user_hasretweeted[u] = 0
user_wasretweeted = {}
for u in nodes: user_wasretweeted[u] = 0
retweets_nodes = set()
for line in lines:
	row = line.split('\t')	
	u1 = row[1]
	u2 = row[2][:-1]
	retweets_nodes.add(u1)
	retweets_nodes.add(u2)
	if u1 in nodes and u2 in nodes:
		user_hasretweeted[u1] += 1
		user_wasretweeted[u2] += 1
		if (u2,u1) in edges_weights: edges_weights[(u2,u1)] += 1
		else: edges_weights[(u2,u1)] = 1

infile = open('data/retweets-mentions/mentions2011_userid.tsv','r')
lines = infile.readlines()
user_hasmentioned = {}
for u in nodes: user_hasmentioned[u] = 0
user_wasmentioned = {}
for u in nodes: user_wasmentioned[u] = 0
mentions_nodes = set()
for line in lines:
	row = line.split('\t')
	u1 = row[1]
	u2 = row[2][:-1]
	mentions_nodes.add(u1)
	mentions_nodes.add(u2)
	if u1 in nodes and u2 in nodes:
		user_hasmentioned[u1] += 1
		user_wasmentioned[u2] += 1
		if (u1,u2) in edges_weights: edges_weights[(u1,u2)] += 1
		else: edges_weights[(u1,u2)] = 1

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

filtered_nodes = set()
incoming_info_vector = []; outgoing_info_vector = []
for u in nodes:
	incoming_info = user_hasretweeted[u]+user_wasmentioned[u]
	outgoing_info = user_wasretweeted[u]+user_hasmentioned[u]
	incoming_info_vector.append(incoming_info)
	outgoing_info_vector.append(outgoing_info)
	if incoming_info > 8 and outgoing_info > 8:
		filtered_nodes.add(u)
print 'number of nodes:',len(filtered_nodes)
filtered_edges = []
for n1 in filtered_nodes:
	if n1 in neighbors:
		for n2 in set(neighbors[n1]).intersection(filtered_nodes):
			filtered_edges.append((n1,n2))
print 'number of edges:',len(filtered_edges)

integers_distribution(incoming_info_vector,'incoming_info')
integers_distribution(outgoing_info_vector,'outgoing_info')

g = igraph.Graph(directed=True)
g.add_vertices(list(filtered_nodes))
g.add_edges(filtered_edges)
components = g.clusters()
maxsize = 0
for c in components:
	if len(c) > maxsize:
		maxsize = len(c)
		giant_component = c
print 'giant connected component size:',maxsize

final_edge_list = []
final_weights_list = []

checkind = 0
giant_components_nodes = []
outfile = open('twitter_network_filtered.txt','w')
outfile.write('#nodes (user ids)\n')
for i in giant_component:
	outfile.write('%s\n' % g.vs[i]['name'])
	giant_components_nodes.append(g.vs[i]['name'])
outfile.write('#edges\n')
for i in giant_component:
	n1 = g.vs[i]['name']
	for n2 in set(neighbors[n1]).intersection(giant_components_nodes):
		outfile.write('%s\t%s\n'%(n1,n2))
		try:
			final_weights_list.append(edges_weights[(n1,n2)])
			final_edge_list.append((n1,n2))
		except:
			pass
outfile.close()
print 'file printed'

network = igraph.Graph(directed=True)
network.add_vertices(giant_components_nodes)
network.add_edges(final_edge_list)
network.es['weight'] = final_weights_list
#network.write_pajek('twitter_network_contentfull_weighted.net')
network.write_ncol('twitter_network_contentfull_weighted.txt')
