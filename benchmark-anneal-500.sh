#!/bin/sh

for temp in 40 44 48 52 56; do
    for alpha in 0.999 0.9975 0.995 0.9925 0.99 0.975 0.95 0.925 0.9; do
        echo '' > results/anneal500-${temp}:${alpha}.txt
        for i in 1 2 3 4 5 6 7 8 9 10; do
            echo ${temp}:${alpha} $i
            python tsp.py -o results/city500-anneal-${temp}:${alpha}-${i}.png -n 500000 -m reversed_sections -a anneal --cooling ${temp}:${alpha} city500.txt >> results/anneal500-${temp}:${alpha}.txt
            sleep 0.1
        done
    done
done