#!/bin/sh
# Build and bzip2 the LULESH binary
BIN=lulesh2.0
TMP=/tmp
REPO=https://github.com/LLNL/LULESH.git
CWD=`pwd`

echo $PWD
cd $TMP
git clone $REPO
cd LULESH
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DMPI_CXX_COMPILER=`which mpicxx` ../
make

mkdir code
cp $BIN code
# Create a run script
cat >> code/run.sh <<EOF
#!/bin/sh

exec ./$BIN \$2 > \$1 2>&1
EOF
chmod 755 code/run.sh
# Wrap up the code
tar -cf $CWD/code.tar.bz2 code
