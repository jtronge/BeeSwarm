#!/bin/sh
# Build and bzip2 the LULESH binary
BIN=lulesh2.0
TMP=/tmp
REPO=https://github.com/LLNL/LULESH.git
PWD=`pwd`

cd $TMP
git clone $REPO
cd LULESH
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DMPI_CXX_COMPILER=`which mpicxx` ../
make
# Wrap up the code
mkdir code
cp $BIN code
tar -cf $PWD/code.tar.bz2 code
