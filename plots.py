import matplotlib
matplotlib.use('TkAgg')

from pylab import *

from sa import P

coords=[x*0.1 for x in range(0,100)]

plot(coords,[P(x,0,1) for x in coords],'b-')
xlabel('difference')
ylabel('probability')

show()