#!/bin/sh
REPO_ROOT=`pwd`

# Load the configuration
. ./beeswarm.conf

# Set up BEE and dependencies
. ./beeswarm/charliecloud.sh
. ./beeswarm/bee-setup.sh

# Launch the BeeSwarm Python script
./beeswarm.py $WFM_PORT

cat ~/.beeflow/*.json
