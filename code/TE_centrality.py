from itertools import islice
import numpy

with open('../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_4_withMMBIAS.dat') as ofile:
	# The header for this file is 
	# 
	# followed_by, follower, transfer_entropy,transfer_entropy_corrected(MM)

	incoming_dict = {}
	outgoing_dict = {}

	for line in islice(ofile, 1, None):
		fromid, toid, TE_B, TE = map(str.strip, line.split(','))

		TE = float(TE)

		if numpy.isnan(TE):
			print 'Warning: Transforming a nan into 0.'

			TE = 0.
		elif TE < 0.:
			TE = 0.

		if fromid in outgoing_dict:
			outgoing_dict[fromid].append(TE)
		else:
			outgoing_dict[fromid] = [TE]

		if toid in incoming_dict:
			incoming_dict[toid].append(TE)
		else:
			incoming_dict[toid] = [TE]

incoming_centrality = []; outgoing_centrality = []

userids = incoming_dict.keys()

for userid in userids:
	incoming_centrality.append(numpy.mean(incoming_dict[userid]))

	outgoing_centrality.append(numpy.mean(outgoing_dict[userid]))

print 'The min and max incoming centralities are: {} / {}'.format(numpy.min(incoming_centrality), numpy.max(incoming_centrality))
print 'The min and max outgoing centralities are: {} / {}'.format(numpy.min(outgoing_centrality), numpy.max(outgoing_centrality))

import pylab

pylab.plot(incoming_centrality, outgoing_centrality, '.')
pylab.xlabel('Influencability'); pylab.ylabel('Influence')
pylab.plot([0, numpy.max(incoming_centrality)], [0, numpy.max(outgoing_centrality)], 'r-')
pylab.show()

order_incoming_centrality = numpy.argsort(incoming_centrality)[::-1]
order_outgoing_centrality = numpy.argsort(outgoing_centrality)[::-1]

K = 10

print 'The top {} influential users are:'.format(K)

for ind in range(K):
	print userids[order_outgoing_centrality[ind]], outgoing_centrality[order_outgoing_centrality[ind]], len(outgoing_dict[userids[ind]])

print '\n\nThe top {} most influenced users are:'.format(K)

for ind in range(K):
	print userids[order_incoming_centrality[ind]], incoming_centrality[order_incoming_centrality[ind]], len(incoming_dict[userids[ind]])

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Investigating numpy.nan showing up in transfer
# entropy file.
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# for ind, userid in enumerate(incoming_dict.keys()):
# 	if numpy.isnan(incoming_centrality[ind]):
# 		print userid

# with open('../data/content-free/directedweightsTE/edge_weights_bin10minutes_lag_4_withMMBIAS.dat') as ofile:
# 	for line in islice(ofile, 1, None):
# 		fromid, toid, TE_B, TE = map(str.strip, line.split(','))

# 		TE = float(TE)

# 		if toid == '105623556':
# 			print fromid, toid, TE_B, TE