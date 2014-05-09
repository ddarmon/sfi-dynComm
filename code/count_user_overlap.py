# A script to count the number of users
# shared pairwise between groups.
#
#	DMD, 130114-10-28

from collections import Counter

# comm_types = ['0', '4', '7', '10']
comm_types = ['4-b1']

for comm_type in comm_types:
	label_file = '/Users/daviddarmon/Documents/Reference/R/Research/2014/network/commplexity/communities/communities{}_comp.txt'.format(comm_type)

	comms = []

	overlaps = []

	with open(label_file) as ofile:
		for line in ofile:
			users = map(str.strip, line.split(' '))

			if len(users) == 1:
				break
			
			comms.append(set(users))

	for i in range(len(comms)):
		for j in range(i+1, len(comms)):
			overlaps.append(len(comms[i].intersection(comms[j])))

	overlaps_by_size = Counter()

	for overlap in overlaps:
		overlaps_by_size[overlap] += 1

	print 'For community type {}, which has {} non-singleton communities, the size of the overlaps are:'.format(comm_type, len(comms))

	print overlaps_by_size, '\n\n'