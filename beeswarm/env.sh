#!/bin/sh
# Set up the environment and important variables

python() {
    python3 $@
}

# Set important environment variables
export REPO_ROOT=`pwd`
# Set the BUILD_DIR for the Charliecloud and BEE installation
export BUILD_DIR=$REPO_ROOT/build
# For the beeswarm.py script
export PATH=$REPO_ROOT:$PATH
# Charliecloud registry authentication
export CH_IMAGE_USERNAME=`beeswarm.py cfg -k ch_image_username`
export CH_IMAGE_PASSWORD=`beeswarm.py cfg -k ch_image_password`
# Needed for ch-builder2tar (until it is deprecated)
export CH_BUILDER=ch-image
# Google application credentials
export GOOGLE_APPLICATION_CREDENTIALS=$REPO_ROOT/google_cred.json
# Cloud configuration file
export CLOUD_CONF=$REPO_ROOT/cloud.yml
