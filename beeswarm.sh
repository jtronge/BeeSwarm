#!/bin/sh
# Workflow init script

# Set important environment variables
REPO_ROOT=`pwd`
# For the beeswarm_conf.py script
export PATH=$REPO_ROOT:$PATH
# Charliecloud registry authentication
export CH_IMAGE_USERNAME=`beeswarm_conf.py ch_image_username`
export CH_IMAGE_PASSWORD=`beeswarm_conf.py ch_image_password`

# Set up BEE and dependencies
. ./beeswarm/charliecloud.sh
. ./beeswarm/bee-setup.sh

python -m beeflow.scheduler.scheduler

sleep 10

# Launch the BeeSwarm Python script
# ./beeswarm.py $WFM_PORT

# cat ~/.beeflow/*.json
