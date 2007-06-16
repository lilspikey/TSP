#!/bin/sh

echo '' > results/hillclimb30-swapped_cities.txt
echo '' > results/hillclimb100-swapped_cities.txt
echo '' > results/hillclimb500-swapped_cities.txt

echo '' > results/hillclimb30-reversed_sections.txt
echo '' > results/hillclimb100-reversed_sections.txt
echo '' > results/hillclimb500-reversed_sections.txt

for i in 1 2 3 4 5 6 7 8 9 10; do
    for move in swapped_cities reversed_sections; do
        echo 30 $move $i
        python tsp.py -o results/city30-${move}-${i}.png -n 1000 -m $move city30.txt >> results/hillclimb30-${move}.txt
        echo 100 $move $i
        python tsp.py -o results/city100-${move}-${i}.png -n 50000 -m $move city100.txt >> results/hillclimb100-${move}.txt
        echo 500 $move $i
        python tsp.py -o results/city500-${move}-${i}.png -n 1000000 -m $move city500.txt >> results/hillclimb500-${move}.txt
    done
done