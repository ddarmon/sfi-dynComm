# A simple model from *Transfer Entropy as a Log-likelihood Ratio*
# by Lionel Barnett and Terry Bossomaier.

import numpy
import sys
import os

N = 500000

epsilons = numpy.zeros(N, dtype = 'int8')
epsilons[numpy.random.rand(N) < 0.5] = 1

etas = numpy.zeros(N, dtype = 'int8')
etas[numpy.random.rand(N) < 0.5] = 1

theta = 0.4
phi   = 0.6

us = numpy.zeros(N, dtype = 'int8')
us[numpy.random.rand(N) < theta] = 1

vs = numpy.zeros(N, dtype = 'int8')
vs[numpy.random.rand(N) < phi] = 1

Xs = numpy.zeros(N, dtype = 'int8')
Xs[0] = numpy.random.randint(2)

Ys = numpy.zeros(N, dtype = 'int8')
Ys[0] = numpy.random.randint(2)

for t in range(1, N):
	Xs[t] = us[t]*Ys[t-1] + (1 - us[t])*epsilons[t]
	Ys[t] = vs[t]*Xs[t-1] + (1 - vs[t])*etas[t]

with open('X.dat', 'w') as wfileX:
	with open('Y.dat', 'w') as wfileY:
		with open('Z.dat', 'w') as wfileZ:
			for t in range(N):
				Xt = Xs[t]
				Yt = Ys[t]

				wfileX.write('{}'.format(Xt))
				wfileY.write('{}'.format(Yt))

				if (Xt == 0) and (Yt == 0):
					Zt = 0
				elif (Xt == 0) and (Yt == 1):
					Zt = 1
				elif (Xt == 1) and (Yt == 0):
					Zt = 2
				elif (Xt == 1) and (Yt == 1):
					Zt = 3
				else:
					print 'Nope!'

					sys.exit(1)

				wfileZ.write('{}'.format(Zt))