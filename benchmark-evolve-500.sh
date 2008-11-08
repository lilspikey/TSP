#!/bin/sh

for popsize in 4 8 12 14 16; do
    echo '' > results/evolve500-${popsize}.txt
    for i in 1 2 3 4 5 6 7 8 9 10; do
        echo evolve ${popsize} $i
        python tsp.py -o results/city500-evolve-${popsize}-${i}.png -n 500000 -m reversed_sections -a evolve --popsize=${popsize} city500.txt >> results/evolve500-${popsize}.txt
        sleep 0.1
    done
done