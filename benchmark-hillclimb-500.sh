#!/bin/sh

echo '' > results/hillclimb500.txt
for i in 1 2 3 4 5 6 7 8 9 10; do
    echo hillclimb $i
    python tsp.py -o results/city500-hillclimb-${i}.png -n 500000 -m reversed_sections -a hillclimb city500.txt >> results/hillclimb500.txt
    sleep 0.1
done