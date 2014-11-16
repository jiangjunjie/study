#!/bin/sh

ulimit -c unlimited
ulimit -f unlimited

g++ main.cpp ACOSearch.cpp Ant.cpp -o test && 
./test eil51.tsp 1>std
