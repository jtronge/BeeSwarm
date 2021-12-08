#!/bin/sh
# Workflow init script

python() {
    python3 $@
}

# Set important environment variables
export REPO_ROOT=`pwd`

# Create the virtual env
rm -rf $REPO_ROOT/venv
python -m venv $REPO_ROOT/venv
. $REPO_ROOT/venv/bin/activate
pip install --upgrade pip
pip install -r $REPO_ROOT/requirements.txt

# Set the BUILD_DIR for the Charliecloud and BEE installation
export BUILD_DIR=$REPO_ROOT/build
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# For the beeswarm_conf.py script
export PATH=$REPO_ROOT:$PATH

# Charliecloud registry authentication
export CH_IMAGE_USERNAME=`beeswarm.py cfg -k ch_image_username`
export CH_IMAGE_PASSWORD=`beeswarm.py cfg -k ch_image_password`

# Needed for ch-builder2tar (until it is deprecated)
export CH_BUILDER=ch-image

# Google application credentials
export GOOGLE_APPLICATION_CREDENTIALS=$REPO_ROOT/google_cred.json
beeswarm.py cfg -k google_application_credentials_base64 | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS

# Configure git
git config --local user.email "`beeswarm.py cfg -k email`"
git config --local user.name "`beeswarm.py cfg -k name`"

# Create the SSH private key file for the cloud
KEY_FILE=`beeswarm.py cfg -k cloud_launcher_conf.private_key_file`
OLD_UMASK=`umask`
umask 0077
beeswarm.py cfg -k private_key_data > $KEY_FILE
umask $OLD_UMASK

# Set up BEE and dependencies
. ./beeswarm/charliecloud.sh
. ./beeswarm/bee-setup.sh

# Output the cloud config
CLOUD_CONF=$REPO_ROOT/cloud.yml
beeswarm.py cfg --cloud-conf > $CLOUD_CONF
#CLOUD_CONFIG=`beeswarm.py cfg -k cloud_config_path`
# python -m beeflow.task_manager &
#beeflow-cloud --tm $CLOUD_CONFIG &
beeswarm.py scale-tests --cloud-conf-path $CLOUD_CONF

exit 1


# Launch the BeeSwarm Python script
# ./beeswarm.py $WFM_PORT

# cat ~/.beeflow/*.json

# Upon completion of the scale tests, commit all results to the `results` branch
# in the results folder
git checkout results
# touch results/testfile
# git add results/testfile
git add results/*
git commit -am "BeeSwarm test results: `date +%F_%T`"
git push -u origin results

