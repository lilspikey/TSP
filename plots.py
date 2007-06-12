import matplotlib
matplotlib.use('TkAgg')

from pylab import *

coords=range(-10,11)

import math

def f(x):
    return x*(math.sin(x/2.0)**2)

plot(coords,[f(x) for x in coords],'b-',[-6],[f(-6)],'ro')

show()