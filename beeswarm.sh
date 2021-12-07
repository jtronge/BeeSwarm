#!/bin/sh
# Workflow init script

# Set important environment variables
REPO_ROOT=`pwd`
# For the beeswarm_conf.py script
export PATH=$REPO_ROOT:$PATH
# Charliecloud registry authentication
export CH_IMAGE_USERNAME=`beeswarm_conf.py ch_image_username`
export CH_IMAGE_PASSWORD=`beeswarm_conf.py ch_image_password`
# Google application credentials
export GOOGLE_APPLICATION_CREDENTIALS=$HOME/google_cred.json
beeswarm_conf.py google_application_credentials_base64 | base64 -d >> $GOOGLE_APPLICATION_CREDENTIALS

# Set up BEE and dependencies
. ./beeswarm/charliecloud.sh
. ./beeswarm/bee-setup.sh

python -m beeflow.task_manager &

sleep 10

# Launch the BeeSwarm Python script
# ./beeswarm.py $WFM_PORT

# cat ~/.beeflow/*.json
