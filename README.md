# verify_gravel
Verification of Compressed Bricks - class project for CS6110

Read more in this [proposal](https://docs.google.com/document/d/1uZaDDlo5LlQEcIfZqqymmbaPRtcTG0j47xhOMQLZwlo/edit?usp=sharing) and [slides](https://docs.google.com/presentation/d/1a98UeDvrW7s5jxWdjcV4WV_5v_Rpp96wxW16cZ6gFFE/edit?usp=sharing) and detailed [report]().
# Running instructions


If cloned
git submodule update --init --recursive


ml gcc/11.2.0 openmpi cuda python3.11.7

# Installation and running

```
# login onto a CHPC node.
ssh kp326

# clone the repo
git clone --recursive -j8 https://github.com/Sameeranjoshi/verify_gravel.git
#If already cloned.
#git submodule update --init --recursive
cd verify_gravel/bricklib

# build bricklib
ml gcc/11.2.0 openmpi cuda python/3.11.7
mkdir -p build/
mkdir -p install/
cd build/
cmake ../ -DCMAKE_INSTALL_PREFIX=../install/
make -j32
make install -j32

# Use bricklib as library
#export brick_DIR=<PATH TO BRICKLIB INSTALL FOLDER>
export brick_DIR=../../../install/lib64/brick/cmake/
mkdir -p ../examples/external/build
cd ../examples/external/build
cmake ../ && make -j12 && cd ../../../

# Run e2e pipeline
## Run single test
./bricklib/examples/external/build/example

## Run experiments e2e and generate excel.
cd bricklib
python3 run_and_generate_csv.py
(check SDD_outputs.xlsx)
```
