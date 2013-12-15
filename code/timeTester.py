import timeit

setup = '''
import random
import pickle
SPARSE_BINARY_HISTORY_PICKLE ="test_histories_factor_600.p"
d = pickle.load(open(SPARSE_BINARY_HISTORY_PICKLE, "rb" ) )
#random.seed('slartibartfast')
#s = [random.random() for i in range(1000)]
#timsort = list.sort

tweets = set()
tweets2 = []
for x in d: tweets.add(x);
##print tweets
tweets2 = sorted(d.keys());
#print tweets2

for x in tweets:
     if x not  in tweets2: print "False"

for x in tweets2:
     if x not in tweets: print "False"
'''
#code = 'a=s[:];timsort(a)'
code1 = 'for x in d: tweets.add(x);'
code2 = 'tweets2 = sorted(d.keys());'
print "code1:", min(timeit.Timer(code1, setup=setup).repeat(7, 1000))
print "code2:", min(timeit.Timer(code2, setup=setup).repeat(7, 1000))

