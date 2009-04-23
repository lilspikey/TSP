#!/bin/sh

for tournament in 150 175 200 225 250 275 300; do
    echo '' > results/evolve100-tournament${tournament}.txt
    for i in $(jot 100 1 100); do
        echo evolve ${tournament} $i
        python tsp.py -o results/city100-evolve-tournament${tournament}-${i}.png -n 100000 -m reversed_sections -a evolve --popsize=1000 --tournament=${tournament} city100.txt >> results/evolve100-tournament${tournament}.txt
        sleep 0.1
    done
done