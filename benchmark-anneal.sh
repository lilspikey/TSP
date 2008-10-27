#!/bin/sh

for temp in 40 44 48 52 56; do
    for alpha in 0.999 0.99925 0.9995 0.99975 0.9999 0.999925 0.99995 0.999975 0.99999; do
        echo '' > results/anneal100-${temp}:${alpha}.txt
        for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
            echo ${temp}:${alpha} $i
            python tsp.py -o results/city100-${temp}:${alpha}-${i}.png -n 50000 -m reversed_sections -a anneal --cooling ${temp}:${alpha} city100.txt >> results/anneal100-${temp}:${alpha}.txt
        done
    done
done