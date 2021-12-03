#!/bin/sh
REPO_ROOT=`pwd`

# Load the configuration
. ./beeswarm.conf

# Set up BEE and dependencies
. ./beeswarm/charliecloud.sh
. ./beeswarm/bee-setup.sh

# Build the container
./beeswarm.py $WFM_PORT

#cd $REPO_ROOT/containers/lulesh
#ch-image build --force -t lulesh .

#cd $REPO_ROOT/containers/beeswarm
#ch-image build --force -t beeswarm .
#ch-builder2tar -b ch-image beeswarm .
#ch-tar2dir beeswarm.tar.gz .
#ch-run beeswarm -- cat /etc/os-release

# Generate workflow
# TODO

# Run workflow with ci-client.py
# TODO

# Save results
# TODO
