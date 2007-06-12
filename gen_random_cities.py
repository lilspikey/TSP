#!/usr/bin/python

import sys
import random

if len(sys.argv) != 4:
    print "usage: python %s <num_cities> <width> <height>" % sys.argv[0]
    sys.exit(1)

num_cities,width,height=sys.argv[1:4]

num_cities=int(num_cities)
width,height=float(width),float(height)

for i in range(num_cities):
    x,y=random.random()*width,random.random()*height
    print '%f,%f' % (x,y)
