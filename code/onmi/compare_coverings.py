import subprocess
import sys
import numpy
import pylab

from StringIO import StringIO

# NOTE: Use code on CSS computer in the Code
# directory to generate these normalized
# mutual informations based off
#
# 	https://github.com/aaronmcdaid/Overlapping-NMI
#

# singleton_type = 'singletons'
singleton_type = 'no_singletons'

num_types = 11

mis = numpy.ones((num_types, num_types))*numpy.nan

with open('mis_{}.txt'.format(singleton_type)) as ofile:
	for ind1 in range(0, num_types):
		for ind2 in range(0, num_types):
			line = ofile.readline().strip()
			mi = float(line)

			mis[ind1, ind2] = mi

print mis

# mis[mis == 1] = numpy.nan
# mis[mis == 0] = numpy.nan

pylab.figure()
pylab.imshow(mis, interpolation = 'nearest', vmin = 0, vmax = 1, cmap = pylab.cm.gray_r)#, extent = (0, num_types, num_types, 0))
pylab.xlabel('Weighting $j$'); pylab.ylabel('Weighting $i$')
pylab.colorbar()
pylab.savefig('nmi_{}.pdf'.format(singleton_type))
# pylab.show()