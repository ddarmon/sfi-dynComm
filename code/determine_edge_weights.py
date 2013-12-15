from __future__ import division
from collections import defaultdict
import datetime
import numpy
import sys
import os
import igraph
import pickle
import pylab
import math
import random
from itertools import islice

MAKE_BINARY_DICT = False
USE_10MIN_DICT = True
Testuid1 = '456'
Testuid2 = '237962820'
Testuid3 = '243494256'
strangeuid ='51319087'
reference_start = datetime.datetime(2011, 4, 25, 9, 24, 58)
reference_stop = datetime.datetime(2011, 6, 25, 14, 31, 59)
#SPARSE_BINARY_HISTORY_PICKLE ="../data/tweet_times_2011/sparse_binary_ts_dict_bin-space-of-10min.p"
#SPARSE_BINARY_HISTORY_PICKLE ="../data/tweet_times_2011/sparse_binary_ts_dict_bin-space-of-1.p"
#SPARSE_BINARY_HISTORY_PICKLE ="test_histories_factor_600.p"
#SPARSE_BINARY_HISTORY_PICKLE ="test_histories_factor_600_set_version.p"
SPARSE_BINARY_HISTORY_PICKLE = "../data/tweet_times_2011/sparse_binary_ts_dict_bin-space-of-10min_set_version.p"
T = (reference_stop - reference_start).total_seconds()

factor = 600 #this corresponds to the 10-minute history
#factor = 1
#factor = int(5288821/4)
full_length = int(T/factor)

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def  make_test_set(full_history):
    test_dict ={}
    n_items = take(50, full_history.iteritems())
    #print n_items
    for user in n_items:
        print user[0]
        test_dict[user[0]] = full_history[user[0]]

    pickle.dump(test_dict, open("test_histories_factor_600_set_version.p", "wb" ) )



def coarsen_sparse_dict(sparse_tweet_history_1_sec, factor):
    coarse_sparse_dict = {}
    for user in sparse_tweet_history_1_sec:
        #print "starting the analysis of user**************:",user
        coarse_sparse_dict[user]=coarse_sparse_resolution(sparse_tweet_history_1_sec[user],T,factor)
    return coarse_sparse_dict

def coarse_sparse_resolution(binary_tweets,orig_size, factor):
    #orig_size = T
    d = {}
    n_coarsebins =int(orig_size/factor)
    #floor(numpy.divide(orig_size, factor))
    #print "n_coarsebins: ",n_coarsebins
    i = 0 
    for x in binary_tweets:
        #This completely corsenes the time series and doesn't take into account how many tweets occured in the larger interval
        #print x, i*n_coarsebins
        
        #if x < i*n_coarsebins: d[i*n_coarsebins] = 1
        #else: i = i+1
        home_found = False
        while not home_found:
            if x <= i*factor:
                #d[i*factor] = 1
                d[i]=1
                home_found = True
                #print "putting ", x," in bin ", i

            else: i = i+1
    #print "d.keys()",d.keys()
    #exit()
    tweets = set()
    for tweet in d:
        tweets.add(tweet)
    return tweets
    #return sorted(d.keys())


def coarsen_analysis(sparse_tweet_history_1_sec):
    #factor = int(5288821/3)
    num_users=len(sparse_tweet_history_1_sec)-1
    f = open('binCoarsenAnalysisv2.dat', 'w')
    f.write("n_coarsebins, factor, AILR\n")
    for factor in xrange(2,50000,10):
        n_coarsebins =int(T/factor)
        #print "n_coarsebins =int(orig_size/factor)" ,n_coarsebins
        information_loss_ratio =0
        coarsened_histories=coarsen_sparse_dict(sparse_tweet_history_1_sec,factor)
        for user in sparse_tweet_history_1_sec:
            if user != '51319087':
                num_full_bins_at_coarsen = len(coarsened_histories[user])
                num_full_bins_at_full = len(sparse_tweet_history_1_sec[user])
                #print"corase/full",num_full_bins_at_coarsen,"/",num_full_bins_at_full
                information_loss_ratio = information_loss_ratio + num_full_bins_at_coarsen/num_full_bins_at_full
        avg_information_loss = 1- information_loss_ratio/num_users
        f.write(str(n_coarsebins))
        f.write(", ")
        f.write(str(factor))
        f.write(", ")
        f.write(str(avg_information_loss))
        f.write("\n")
        print "Finished with factor",factor
        print "     information_loss_ratio",information_loss_ratio
        print "     num_users", num_users
        print "     avg_information_loss: ",avg_information_loss
    f.close()

def make_binary_vector_big(tweetBins,reduction_factor):
    #This should take a vector of indicies made from create_binary_ts_from_arrival_times and return a binary array
    binary = numpy.zeros((T+1)/reduction_factor, dtype = 'int8') #with coarsening this will change....
    binary[tweetBins]=1
    return binary

def create_binary_ts_from_arrival_times(uid,erroridfile):
	tweets = [] # A placeholder for the times of the tweets.
        # Keep track of the total number of seconds elapsed from the reference
	# start to the reference stop.


	# binary is a length T vector with a 0 at index n if 
	# a Tweet occurred and a 1 otherwise.
	binary = numpy.zeros(T+1, dtype = 'int8')
        
        try:
            with open('../data/tweet_times_2011/tweet_times_{}.dat'.format(uid)) as ofile:
		for line in ofile:
			tweets.append(int(line)) # Read in all of the times of the tweets.
            binary[tweets]=1
        except IOError:
            erroridfile.write(uid+'\n')
            # generate a file of all 

        #with open('tweet_times_2011/tweet_times_{}.dat'.format(uid)) as ofile:
        #for line in ofile:
        #tweets.append(int(line)) # Read in all of the times of the tweets.




	#binary[tweets] = 1

	#return binary
        return tweets
# To save to a file. Though you're probably
# better just generating binary each time 
# you need to do any computations rather 
# than writing and then reading from the file.

# with open('tweet_times_2011/tweet_times_binary_{}.dat'.format(uid), 'w') as wfile:
# 	for bit in binary:
# 		wfile.write('{}'.format(bit))


#binary = create_binary_ts_from_arrival_times(uid)




def make_sparse_binary_ts_dict(nodes):
    errorfile= open("nodesWithoutTweetHistory.txt", "w")
    ts_dict = {}
    i = 0
    #testnode = Testuid
    for node in nodes:
        ts_dict[node] = create_binary_ts_from_arrival_times(node,errorfile)
        i = i+1
        print i,len(nodes)
    #ts_dict[node] = create_binary_ts_from_arrival_times(node,errorfile)
    #print len(ts_dict[node])
    print "Finished Building Sparse Tweet History, now writing to pickle."
    pickle.dump(ts_dict, open( "../data/tweet_times_2011/sparse_binary_ts_dict_bin-space-of-1.p", "wb" ) )
    
    
    #f = open('portData.pkl','r')
    #data = pickle.load(f)
    #read_dict = pickle.load( open( "sparse_binary_ts_dict.p", "rb" ) )
    #print read_dict
    errorfile.close()
    return ts_dict

def get_tweet_history():
    return pickle.load(open(SPARSE_BINARY_HISTORY_PICKLE, "rb" ) )


def H_transfer_entropy(prob_mass_function):
    H = 0
    for perm in prob_mass_function:
        H += prob_mass_function[perm]*numpy.log2(prob_mass_function[perm])
    return -H

def joint_mass_function(XT,YT):
    #This should calculate the joint mass funciton of three variables
    #In particular P(X_{t-1},Y_{t-1},Yt)
    #   XT should be the  sparse_binary_tweet history of the followed_by
    #   YT should be the sparse_binary_tweet history of the follower. 
    #   we then form a tuple with(X_{t-1},Y_{t-1},Y_t) =((0,1),(1,1),0)
    #   in the simple case this is ((0),(1),0). Each element in the lag adds a new symbol
    #   to the x_t-1 random variable alphabet
    #   full_length = 
    counts = defaultdict(int)

    nonzero_count = 0
    for y in YT:
        #print y,y-1,
        yt = (1)
        #yt_1 = (1)
        if y-1 in YT:
            yt_1 = 1
        else:
            yt_1 = 0
        if y-1 in XT:
            xt_1 = (1)
        else:
            xt_1 = (0)
        stencil = (xt_1,yt_1,yt)
        #print(stencil),(y-1,y-1,y)
        nonzero_count +=1
        counts[stencil] +=1
        if y+1 not in YT:
            yt = (0)
            yt_1 = (1)
            if y in XT:
                xt_1 = (1)
            else:
                xt_1 = (0)
            stencil = (xt_1,yt_1,yt)
            #print(stencil),(y,y,y+1)
            nonzero_count +=1
            counts[stencil] +=1
    for xt in XT:
        #print "xt",xt
        if xt not in YT and xt+1 not in YT:
            #print(xt)
            xt_1 = (1)
            yt_1 = (0)
            yt = 0
            stencil = (xt_1,yt_1,yt)
            #print(stencil),xt
            counts[stencil] +=1
            nonzero_count +=1

    zero_stencil = ((0),(0),0)
    counts[zero_stencil] = full_length-nonzero_count
    #print(full_length)
    #print "Tweets for X:",len(XT)
    #print "Tweet History for X:",XT
    #print "Tweet History for Y:", YT
    #print "Tweets for Y:",len(YT)
    #print(counts)
    full_joint_prob_mass_func = {}
    for perm in counts:
        full_joint_prob_mass_func[perm]=counts[perm]/full_length
    #prob_total = 0
    #for perm in full_joint_prob_mass_func:
    #    prob_total += full_joint_prob_mass_func[perm]
    
        #marginal_dist[(xt_1,yt)]+=c
    #print "marginal_dict on yt_1",marginal_dist
    #print "total_tweets_by y",len(YT)
    #print "probability_func",full_joint_prob_mass_func
    #print"Total Probability",prob_total
    return full_joint_prob_mass_func
    


def joint_mass_function_lagged(XT,YT,lag):
    #This should calculate the joint mass funciton of three variables
    #In particular P(X_{t-1},Y_{t-1},Yt)
    #   XT should be the  sparse_binary_tweet history of the followed_by
    #   YT should be the sparse_binary_tweet history of the follower. 
    #   we then form a tuple with(X_{t-1},Y_{t-1},Y_t) =((0,1),(1,1),0)
    #   in the simple case this is ((0),(1),0). Each element in the lag adds a new symbol
    #   to the x_t-1 random variable alphabet
    #   full_length = 
    counts = defaultdict(int)

    nonzero_count = 0
    for y in YT:
        windowMax = y+1+lag
        for ycheck in range(y+1,y+1+lag):
            if ycheck in YT:
                windowMax = ycheck
                break

        for ytop in range(y,windowMax):
            #print ytop
            xperm = [(1 if tweet_time in XT else 0) for tweet_time in range(ytop-lag,ytop)]
            yperm = [(1 if tweet_time in YT else 0) for tweet_time in range(ytop-lag,ytop+1)]
            #print xperm,range(ytop-lag,ytop)
            #print yperm,range(ytop-lag,ytop+1)
            if sum(yperm) != 0:
                stencil = (tuple(xperm),tuple(yperm[0:-1]),yperm[-1])
                #print "placing this stencil in count:",stencil
                counts[stencil] +=1
                nonzero_count +=1
            #else:
                #stencil = (tuple(xperm),tuple(yperm[0:-1]),yperm[-1])
                #print "skipping this stencil in count:",stencil
    

    for x in XT:
        windowMax = x+lag
        for xcheck in range(x+1,windowMax):
            if xcheck in XT:
                windowMax = xcheck
                break

        for xtop in range(x,windowMax):
            #print xtop
            yperm = [(1 if tweet_time in YT else 0) for tweet_time in range(xtop-lag+1,xtop+2)]
            xperm = [(1 if tweet_time in XT else 0) for tweet_time in range(xtop-lag+1,xtop+1)]
            #print xperm, range(xtop-lag+1,xtop+1)
            #print yperm, range(xtop-lag+1,xtop+2)
            if sum(yperm) ==0:
                stencil = (tuple(xperm),tuple(yperm[0:-1]),yperm[-1])
                #print "placing this stencil in count:",stencil
                counts[stencil] +=1
                nonzero_count +=1
            #else: #print "skipped double count",yperm


    #xperm zeros
    perm = tuple([0] * lag)
    zero_stencil = (perm,perm,0)
    counts[zero_stencil] = full_length-nonzero_count
    #print(full_length)
    #print "Tweets for X:",len(XT)
    #print "Tweet History for X:",XT
    #print "Tweet History for Y:", YT
    #print "Tweets for Y:",len(YT)
    #print(counts)
    full_joint_prob_mass_func = {}
    normalize = full_length-lag
    for perm in counts:
        full_joint_prob_mass_func[perm]=counts[perm]/normalize
    #prob_total = 0
    #for perm in full_joint_prob_mass_func:
    #    prob_total += full_joint_prob_mass_func[perm]
    
        #marginal_dist[(xt_1,yt)]+=c
    #print "marginal_dict on yt_1",marginal_dist
    #print "total_tweets_by y",len(YT)
    #print "probability_func",full_joint_prob_mass_func
    #print"Total Probability",prob_total
    return full_joint_prob_mass_func
    

            
            
            
            

#def calculate_transfer(uid1,uid2):
def transfer_entropy(followed_by_id,follower_id,sparse_histories,lag):
    #Just place holder not actual caluclation
    #Convert both ids histories from sparce to big format.
    #We want infromation to go from $T_{followed_by -> follower}
    #Let X = followed_by and Y = follower
    #T = H(Y_t,Y_{t-1})-H(Y_{t-1})-H(Yt,Y_{t-1},X_{t-1})+H(Y_{t-1},X_{t-1})

    prob_mass_func = joint_mass_function_lagged(sparse_histories[followed_by_id],sparse_histories[follower_id],lag)

    #Get Each marginal we need
    #H(Y_t,Y_{t-1})
    marginal_distytyt_1 = defaultdict(float)
    for (xt_1,yt_1,yt),c in prob_mass_func.items():
        marginal_distytyt_1[(yt_1,yt)]+=c

    #H(Y_{t-1})
    marginal_distyt_1 = defaultdict(float)
    for (xt_1,yt_1,yt),c in prob_mass_func.items():
        marginal_distyt_1[(yt_1)]+=c

    #H(Yt,Y_{t-1},X_{t-1})+
    #prob_mass_func

    #H(Y_{t-1},X_{t-1})
    marginal_distyt_1xt_1 = defaultdict(float)
    for (xt_1,yt_1,yt),c in prob_mass_func.items():
        marginal_distyt_1xt_1[(xt_1,yt_1)]+=c

    #T = H(Y_t,Y_{t-1})-H(Y_{t-1})-H(Yt,Y_{t-1},X_{t-1})+H(Y_{t-1},X_{t-1})
    trans_entropy = H_transfer_entropy(marginal_distytyt_1)-H_transfer_entropy(marginal_distyt_1)-H_transfer_entropy(prob_mass_func)+H_transfer_entropy(marginal_distyt_1xt_1)
    #print uid1,u1TS, s1
    #print uid2,u2TS,s2
    #trans_entropy = s1+s2
    #print trans_entropy
    return trans_entropy


def calculate_weight(edges,sparse_histories,weight_type):
    edge_weights = {}
    if weight_type == 'transfer_entropy':
        for edge in edges:
            if edge[0] in sparse_histories and edge[1] in sparse_histories:
                #edge = (edge[0],edge[1]) = followed_by, follower
                edge_weights[edge]= transfer_entropy(edge[0],edge[1],sparse_histories,3)

    return edge_weights

def build_directed_graph_without_weights():
    #read in filtered nodes
    #nodefile = open('../data/twitter_network_filtered_nodes.txt','r')
    edgefile =  open('../data/twitter_network_filtered_edges.txt','r')
    #nodeLines = nodefile.readlines()
    edgeLines = edgefile.readlines()
    #nodefile.close()
    edgefile.close()
    #nodes is all the filtered nodes
    #neighbors is a dictonary that maps a user to all the people that user follows (maybe ... ask Elisa)
    nodes = set(); edges = []; neighbors = {}
    #neighbors will be a dictionary which maps a userid to a list of followers.
    #edges goes from followed_by--->follower
    #To compare with twitter_network_filtered_edges.txt this is labeled
    #    followed_by      follower
    #        ur                 ul
    #     ###uid1####      ##uid2###
    #nodes is simply a set of uids that we are using. (may not actually be used)
    
    #This for loop might be unnessecary me might be able to just say nodes = neighbors.keys()
    #for line in nodeLines:
    #   row = line.split()
    #	user = row[0]
    #   follower = row[2]
    #	nodes.add(user); #nodes.add(follower)
    #	#edges.append((user,follower))
    #	#if user in neighbors: neighbors[user].append(follower)
    #	#else: neighbors[user] = [follower]
    print "Starting neighbor relation construction."
    for line in edgeLines:
        row = line.split('\t')
	followed_by = row[0]
	follower = row[1][:-1]
        edges.append((followed_by,follower))
        #print followed_by,follower
        #if user in neighbors: neighbors[user].append(follower)
	#else: neighbors[user] = [follower]
        if followed_by in neighbors: neighbors[followed_by].append(follower)
	else: neighbors[followed_by] = [follower]
    for node in neighbors:
        nodes.add(node)
    #nodes = neighbors.keys()
    print "Finished neighbor relation construction."

    #coarsaning should happen here if it is going to happen, the sparse_tweet_history is a sparse representation where
    #each bin is 1 second if this is too rapid the bins should be readjusted using "coarse_resolution"

    #sparse_tweet_history_10_minute=coarsen_sparse_dict(sparse_tweet_history_1_sec)
    #pickle.dump(sparse_tweet_history_10_minute, open( "../data/tweet_times_2011/sparse_binary_ts_dict_bin-space-of-10min.p", "wb" ) )

    #print "size of sparse_tweet_history_1_sec",len(sparse_tweet_history_1_sec[Testuid])
    #print "size of sparse_tweet_history_10_minute", len(sparse_tweet_history_10_minute[Testuid])
    #print "size of coarse tweet historys",len(sparse_tweet_history[Testuid])

    #edges_weights = calculate_weight(edges,sparse_tweet_history,'transfer_entropy')
    #I think I want edge_weights to be a dictionary keyed by an edge and pointing to a weight so
    # {[followed_by,follower]:weight}
    #for node in neighbors.keys():
    #    for follower in neighbors[node]:
    #        weight_test = calculate_edge_weight(node,follower)
    #        print 'Test Weight',weight_test
    # doing it this way actually regrabs a bunch of files for example it regrabs 76 over and over
    #for edge in edges:
        #print edge
        #    weight_test = calculate_edge_weight(edge[0],edge[1])
        #     print 'Test Weight',weight_test
    print 'number of edges:',len(edges)
    print 'number of nodes:',len(nodes)


    
    DWG = {}
    #IF the edge does not go both ways should we still weight the edge
    #DWG = {user:{follows:edge_weight}
    
    #network = igraph.Graph(directed=True)
    #i think this is just the nodes
    #network.add_vertices(giant_components_nodes)
    #network.add_vertices(nodes)
    #network.add_edges(final_edge_list)
    #I think this is just the edges I don't eliminate any 
    #network.add_edges(edges)
    #I still need to caluclate the weights list
    #network.es['weight'] = final_weights_list
    #network.write_pajek('twitter_network_contentfull_weighted.net')
    #network.write_ncol('twitter_network_contentfree_weighted.txt')


    return (nodes,edges,neighbors)

#Construct Graph
users,edges,neighbors = build_directed_graph_without_weights()


#Retrieve Tweet History from Pickle
sparse_tweet_history = get_tweet_history()


#For Testing
#make_test_set(sparse_tweet_history)




#For coarsening

#sparse_tweet_history_10_minute=coarsen_sparse_dict(sparse_tweet_history,600)
#pickle.dump(sparse_tweet_history_10_minute, open( "../data/tweet_times_2011/sparse_binary_ts_dict_bin-space-of-10min_set_version.p", "wb" ))

print "starting edge weight"
edge_weight = calculate_weight(edges,sparse_tweet_history,'transfer_entropy')
print "done"



f = open('edge_weights_10min_lag3.dat', 'w')
f.write("followed_by, follower, transfer_entropy\n")
for edge in edge_weight:
    f.write(str(edge[0]))
    f.write(", ")
    f.write(str(edge[1]))
    f.write(", ")
    f.write(str(edge_weight[edge]))
    f.write("\n")

f.close()
    #print edge,edge_weight[edge]

#coarsen_analysis(sparse_tweet_history)
  
    
