#!/bin/sh

for popsize in 2 5 10 15; do
    echo '' > results/evolve100-${popsize}.txt
    for i in $(jot 100 1 100); do
        echo evolve ${popsize} $i
        python tsp.py -o results/city100-evolve-${popsize}-${i}.png -n 100000 -m reversed_sections -a evolve --popsize=${popsize} city100.txt >> results/evolve100-${popsize}.txt
        sleep 0.1
    done
done