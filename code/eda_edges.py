import os

# weight_type = 'transfer-entropy'
# weight_type = 'hashtag'
weight_type = 'mention-retweet'

print '\nUsing weights of type {}\n'.format(weight_type)

fname = '../data/topK_{}.dat'.format(weight_type)

num_links = 10

with open(fname) as ofile:
	ofile.readline() # Skip the header line.

	for ind in range(num_links):
		from_id, to_id, weight = ofile.readline().strip().split(' ')

		print from_id, to_id, weight

		raw_input("")

		os.system("open 'http://twitter.com/account/redirect_by_id?id={}'".format(from_id))
		os.system("open 'http://twitter.com/account/redirect_by_id?id={}'".format(to_id))