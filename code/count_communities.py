# A script to count the number of non-singleton
# communities for each of the community types.
#
#	DMD, 140114-09-45

from collections import Counter

# comm_types = [0, 4, 7, 10]
comm_types = range(11)

for comm_type in comm_types:
	# Count number of non-singleton communities.

	label_file = 'mutual3/coverings/no_singletons/communitites{}_comp.txt'.format(comm_type)

	comm_count = 0

	with open(label_file) as ofile:
		for line in ofile:
			comm_count += 1

	# print comm_type, comm_count

	# Count number of singleton communities.

	label_file = 'mutual3/coverings/singletons/communitites{}_comp.txt'.format(comm_type)

	singleton_count = 0

	with open(label_file) as ofile:
		for line in ofile:
			if len(line.strip().split(' ')) == 1:
				# print line.split(' ')
				singleton_count += 1

	print comm_type, singleton_count