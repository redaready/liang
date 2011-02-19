# coding: utf8
"""
    回答 https://groups.google.com/forum/?hl=fr#!topic/python-cn/UyXiBqEksXw
"""

from collections import defaultdict
from timeit import timeit

s = """
from itertools import tee,imap

threshold = 4
dsg = xrange(0,%d)

def redar1(dsg,threshold):
    miniiter,maxiter = tee(imap(lambda x: abs(x-threshold), dsg))
    return min(miniiter),max(maxiter)

def redar2(dsg,threshold):
    miniiter,maxiter = tee(map(lambda x: abs(x-threshold), dsg))
    return min(miniiter),max(maxiter)

def redar3(dsg,threshold):
    miniiter,maxiter = tee(abs(x-threshold) for x in dsg)
    return min(miniiter),max(maxiter)

import numpy as np

def redar4(dsg,threshold):
    a = np.abs(np.array(dsg)-threshold)
    return np.amin(a),np.amax(a)

def ruoyu(dsg,threshold):
    return reduce(lambda (lo,hi),x:(min(lo,x),max(hi,x)),
        (abs(x-threshold) for x in dsg), (float("inf"),float("-inf")))

def shell(dsg,threshold):
    l = map(lambda x: abs(x-threshold), dsg)
    return min(l), max(l)

def jackie(dsg,threshold):
    if not dsg: raise ValueError('empty dsg')
    it = iter(dsg)
    v = abs(next(it)-threshold)
    min,max = v,v
    for v in it:
        v = abs(v-threshold)
        if min>v: min=v
        if max<v: max=v
    return min,max

"""

tests = {
    'redar1-tee-imap':'redar1(dsg,threshold)',
    'redar2-tee-map':'redar2(dsg,threshold)',
    'redar3-tee-gen':'redar3(dsg,threshold)',
    'redar4-numpy':'redar4(dsg,threshold)',
    'ruoyu-reduce':'ruoyu(dsg,threshold)',
    'shell-map':'shell(dsg,threshold)',
    'jackie':'jackie(dsg,threshold)'
}

result = defaultdict(list)
x = xrange(1,5001,200)
for n in x:
    print n
    setup = s % n
    for name,test in tests.items():
        result[name].append(timeit(test,setup,number=1000)*1000) # in us
print result
import cPickle
f = open('result.pickle','wb')
cPickle.dump(result,f,protocol=-1)
f.close()

from matplotlib import pyplot as plt
for name,r in result.items():
    plt.plot(x,r,label=name)
plt.legend(loc='upper left')
#plt.show()
plt.savefig('forMaxMin.png')

    