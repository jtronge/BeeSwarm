#!/bin/sh
CWD=`pwd`
# Install Charliecloud
cd /tmp
curl -O -L https://github.com/hpc/charliecloud/releases/download/v0.25/charliecloud-0.25.tar.gz
tar -xvf charliecloud-0.25.tar.gz
cd charliecloud-0.25
./configure --prefix=$HOME
make
make install
export PATH=$HOME/bin:$PATH
cd $CWD
