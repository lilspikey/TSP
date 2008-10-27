#!/bin/sh

echo '' > results/evolve100.txt

for i in $(jot 100 1 100); do
    echo evolve $i
    python tsp.py -o results/city100-evolve-${i}.png -n 100000 -m reversed_sections -a evolve city100.txt >> results/evolve100.txt
done