# verify_gravel
Verification of Compressed Bricks - class project for CS6110
./generate_Host_LC-Framework.py
g++ -O3 -march=native -fopenmp -DUSE_CPU -I. -std=c++17 -o lc lc.cpp
./lc input.dat CR "" ".+ .+"
