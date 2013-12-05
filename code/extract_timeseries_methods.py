import ipdb
import numpy
import pylab
import datetime
import random

def coarse_resolution(binarized, iresolution = 60):
    # Takes in a binary time series with a time step
    # of 1 tick, and returns a binary timeseries
    # with time step iresolution ticks where
    # a 0 is returned of no 1s occur in the bin,
    # and a 1 is otherwise.

    # The number of bins we'll have after coarsening.

    n_coarsebins = numpy.divide(binarized.shape[0], iresolution)

    # An (empty) binary time series to hold the
    # coarsened time series.

    binarized_coarse = numpy.zeros(n_coarsebins)

    for cind in range(n_coarsebins):
        binarized_coarse[cind] = numpy.sum(binarized[(cind*iresolution):((cind + 1)*iresolution)])
    
    # Convert the *number* of tweets in the time interval
    # into *whether* a tweet occurs in that time interval.
    
    binarized_coarse[binarized_coarse != 0] = 1
    
    return binarized_coarse