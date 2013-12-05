# Code to estimate the transfer entropy directly
# by assuming a lag k and computing the plug-in
# estimator for the mass function.
#
# DMD, 111113-23-10

import numpy

k = 2 # The lag to consider

alphabet_x = 2
alphabet_y = 2

dir_name = '../data/te/'

# We'll always use the convention that we're computing
# TE_{Y -> X}, regardless of the names of the variables.

X_filename = 'ts1.dat'
Y_filename = 'ts0.dat'

X = map(int, open('{}{}'.format(dir_name, X_filename)).readline().strip())
Y = map(int, open('{}{}'.format(dir_name, Y_filename)).readline().strip())

# Shorten ts for ease of debugging.

# X = X[:100000]
# Y = Y[:100000]

# Make a 'null' data set where Y should have impact on X.

# numpy.random.shuffle(Y)

N = len(X)

# The stochastic 'matrix' tracking the conditional
# distributions of X_{t} | X_{t-k}^{t-1}. We'll store
# this as a dictionary that takes as a key the 
# past being conditioned on and returns the counts
# over each of the symbols.

# We still order the key as (x_{t-1}, x_{t-2}, ..., x_{t-k}).

cond_X = {}

# The marginal distribution of X_{t-k}^{t-1}. We use 
# the same convention as above for indexing into the
# array.

dims = []

for ind in range(k):
	dims.append(alphabet_x)

dims = tuple(dims)

marg_X = numpy.zeros(dims)

# cond_XY and marg_XY are the same as above,
# but now tracking the distribution of 
# X_{t} | (X_{t-k}^{t-1}, Y_{t-k}^{t-1}).

cond_XY = {}

dims = []

for ind in range(k):
	dims.append(alphabet_x)

for ind in range(k):
	dims.append(alphabet_y)

dims = tuple(dims)

marg_XY = numpy.zeros(dims)

# Populate cond_X and marg_X.

for ind in range(N - k):
# for ind in range(50000):
	# Get out the current history,
	# listed as [x_{t}, x_{t-1}, ...]

	cur_hist = X[ind:(ind+k+1)][::-1]
	cur_hist_tuple = tuple(cur_hist)

	# Populate the various mass function
	# estimators.
	if cur_hist_tuple[1:] in cond_X:
		cond_X[cur_hist_tuple[1:]][cur_hist[0]] += 1
	else:
		cond_X[cur_hist_tuple[1:]] = numpy.zeros(alphabet_x)
		cond_X[cur_hist_tuple[1:]][cur_hist[0]] += 1

	marg_X[tuple(cur_hist[1:])] += 1

	# Do all of the same things, but now with the joint
	# history.

	cur_hist_joint = []

	cur_hist_joint.extend(cur_hist)
	cur_hist_joint.extend(Y[(ind+1):(ind+k+1)][::-1])

	cur_hist_joint_tuple = tuple(cur_hist_joint)

	if cur_hist_joint_tuple[1:] in cond_XY:
		cond_XY[cur_hist_joint_tuple[1:]][cur_hist_joint[0]] += 1
	else:
		cond_XY[cur_hist_joint_tuple[1:]] = numpy.zeros(alphabet_x)
		cond_XY[cur_hist_joint_tuple[1:]][cur_hist_joint[0]] += 1

	marg_XY[tuple(cur_hist_joint[1:])] += 1

# Normalize the marginal pmfs.

marg_X = marg_X / numpy.sum(marg_X)
marg_XY = marg_XY / numpy.sum(marg_XY)

# Normalize the conditional pmfs.

# I think there's something fishy going on with cond_XY, but
# I'm not sure what.

for past in cond_X:
	cond_X[past] = cond_X[past]/numpy.sum(cond_X[past])

for past in cond_XY:
	cond_XY[past] = cond_XY[past]/numpy.sum(cond_XY[past])


def info_log2(p):
	# Use the information theoretic convention that 0 log 0 = 0.

	if p == 0:
		return 0
	else:
		return numpy.log2(p)

# Compute the conditional entropy
# 
# H[X_{t} | X_{t-1}, X_{t-2}, ..., X_{t-k}]
#
# by cycling through all possible histories
# 
# (X_{t}, X_{t-1}, X_{t-2}, ..., X_{t-k}).

H_X = 0

for past in cond_X:
	for future in range(alphabet_x):
		H_X += marg_X[past]*cond_X[past][future]*info_log2(cond_X[past][future])

H_X = -H_X

print 'The conditional entropy H[X_{{t}} | X_{{t-1}}, X_{{t-2}}, ..., X_{{t-k}}] is {}...'.format(H_X)

# Compute the conditional entropy
# 
# H[X_{t} | X_{t-1}, X_{t-2}, ..., X_{t-k}, Y_{t-1}, ..., Y_{t-k}]
#
# by cycling through all possible histories
# 
# (X_{t}, X_{t-1}, X_{t-2}, ..., X_{t-k}, Y_{t-1}, ..., Y_{t-k}).

H_XY = 0

for past in cond_XY:
	for future in range(alphabet_x):
		# Use the convention that 0 log 0 = 0.
		if cond_XY[past][future] == 0:
			pass
		else:
			H_XY += marg_XY[past]*cond_XY[past][future]*info_log2(cond_XY[past][future])

H_XY = -H_XY

print 'The conditional entropy H[X_{{t}} | X_{{t-1}}, X_{{t-2}}, ..., X_{{t-k}}, Y_{{t-1}}, ..., Y_{{t-k}}] is {}...'.format(H_XY)

print 'The estimated transfer entropy is {}...'.format(H_X - H_XY)

# These are the 'population' values for the Barnett process
# that I used to debug this code.

# theta = 0.4; phi = 0.6

# Compute H[X_{t} | X_{t-1}, X_{t-2}].

# p_0 = 0.5*theta*(1-phi) + 0.5*(1-theta)
# p_1 = theta*phi + p_0

# H_X_true = -0.5*(p_0*numpy.log2(p_0) + (1-p_0)*numpy.log2(1-p_0) + p_1*numpy.log2(p_1) + (1-p_1)*numpy.log2(1-p_1))

# Compute H[X_{t} | X_{t-1}, Y_{t-1}]

# o_p_theta = 1 + theta
# o_m_theta = 1 - theta

# H_XY_true = -0.5*(o_p_theta*numpy.log2(0.5*o_p_theta) + o_m_theta*numpy.log2(0.5*o_m_theta))

# print 'The true transfer entropy is {}...'.format(H_X_true - H_XY_true)