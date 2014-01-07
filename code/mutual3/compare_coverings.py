import subprocess
import sys
import numpy
import pylab

from StringIO import StringIO

# singleton_type = 'singletons'
singleton_type = 'no_singletons'

file_dir = 'coverings/{}/'.format(singleton_type)

num_types = 9

mis = numpy.ones((num_types, num_types))*numpy.nan

for ind1 in range(0, num_types):
	fname1 = '{}communitites{}_comp.txt'.format(file_dir, ind1)
	for ind2 in range(0, num_types):
		fname2 = '{}communitites{}_comp.txt'.format(file_dir, ind2)
		sp = subprocess.Popen(['./mutual', fname1, fname2], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
		sp.wait()
		mi = float(sp.communicate()[0].split()[1])

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