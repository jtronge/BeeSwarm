#!/bin/sh
# Launch the BeeSwarm init script inside of a container

CWD=`pwd`
INIT_SCRIPT=${INIT_SCRIPT:-./beeswarm/beeswarm.sh}
CH_RUN_OPTS="-b /var/tmp --cd $CWD"

# Install Charliecloud
export EXTERNAL_CH_DIR=/tmp/charliecloud
export CH_BUILDER=ch-image
export PATH=$EXTERNAL_CH_DIR/bin:$PATH

cd /tmp
rm -rf charliecloud-*
curl -O -L https://github.com/hpc/charliecloud/releases/download/v0.26/charliecloud-0.26.tar.gz
tar -xvf charliecloud-0.26.tar.gz
cd charliecloud-0.26
rm -rf $EXTERNAL_CH_DIR
./configure --prefix=$EXTERNAL_CH_DIR
make
make install

# Now pull and run the container
cd /tmp
ch-image pull jtronge/bee
ch-builder2tar jtronge/bee .
mv jtronge*bee* bee-ctr.tar.gz
ch-tar2dir bee-ctr.tar.gz /tmp
cd $CWD
exec ch-run $CH_RUN_OPTS /tmp/bee-ctr $INIT_SCRIPT
