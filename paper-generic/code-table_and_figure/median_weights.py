import sys

wfile = sys.stdout

with open('../../code/median_weights.txt') as ofile:
	for ind1 in range(4):
		for ind2 in range(3):

			line = ofile.readline()
			label, weight, medians = line.split(', ')

			e_to_i, i_to_e = map(float, medians.split('/'))

			if ind2 == 2:
				wfile.write('${:0.2}/{:0.2}$\\\\\n'.format(e_to_i, i_to_e))
			else:
				wfile.write('${:0.2}/{:0.2}$& '.format(e_to_i, i_to_e))

		# wfile.write('\n')