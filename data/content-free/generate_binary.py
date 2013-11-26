import datetime
import numpy

uid = '456'

def create_binary_ts_from_arrival_times(uid):
	tweets = [] # A placeholder for the times of the tweets.

	with open('tweet_times_2011/tweet_times_{}.dat'.format(uid)) as ofile:
		for line in ofile:
			tweets.append(int(line)) # Read in all of the times of the tweets.

	# Keep track of the total number of seconds elapsed from the reference
	# start to the reference stop.

	reference_start = datetime.datetime(2011, 4, 25, 9, 24, 58)

	reference_stop = datetime.datetime(2011, 6, 25, 14, 31, 59)

	T = (reference_stop - reference_start).total_seconds()

	# binary is a length T vector with a 0 at index n if 
	# a Tweet occurred and a 1 otherwise.

	binary = numpy.zeros(T, dtype = 'int8')

	binary[tweets] = 1

	return binary

binary = create_binary_ts_from_arrival_times(uid)

# To save to a file. Though you're probably
# better just generating binary each time 
# you need to do any computations rather 
# than writing and then reading from the file.

# with open('tweet_times_2011/tweet_times_binary_{}.dat'.format(uid), 'w') as wfile:
# 	for bit in binary:
# 		wfile.write('{}'.format(bit))