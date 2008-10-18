import matplotlib
matplotlib.use('TkAgg')

from pylab import *
import sys
from sa import P, kirkpatrick_cooling

if sys.argv[1] == 'P':
    coords=[x*0.1 for x in range(0,100)]

    plot(coords,[P(x,0,1) for x in coords],'b-')
    xlabel('difference')
    ylabel('probability')

    show()
else:
    cooling=kirkpatrick_cooling(100,0.9)
    coords=range(0,100)

    plot(coords,[t for i,t in zip(coords,cooling)],'b-')
    xlabel('time')
    ylabel('temperature')

    show()