#!/bin/sh
# Workflow init script

# Set important environment variables
REPO_ROOT=`pwd`
# For the beeswarm_conf.py script
export PATH=$REPO_ROOT:$PATH
# Charliecloud registry authentication
export CH_IMAGE_USERNAME=`beeswarm_conf.py -k ch_image_username`
export CH_IMAGE_PASSWORD=`beeswarm_conf.py -k ch_image_password`
# Needed for ch-builder2tar (until it is deprecated)
export CH_BUILDER=ch-image
# Google application credentials
export GOOGLE_APPLICATION_CREDENTIALS=$HOME/google_cred.json
beeswarm_conf.py -k google_application_credentials_base64 | base64 -d >> $GOOGLE_APPLICATION_CREDENTIALS

# Set up BEE and dependencies
. ./beeswarm/charliecloud.sh
. ./beeswarm/bee-setup.sh

sleep 20

# Output the cloud config
CLOUD_CONFIG=`beeswarm_conf.py -k cloud_config_path`
beeswarm_conf.py --cloud-conf >> $CLOUD_CONFIG
# python -m beeflow.task_manager &
beeflow-cloud --tm $CLOUD_CONFIG &

sleep 10


# Launch the BeeSwarm Python script
# ./beeswarm.py $WFM_PORT

# cat ~/.beeflow/*.json
