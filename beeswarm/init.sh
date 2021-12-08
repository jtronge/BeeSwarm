#!/bin/sh
# Initialize and install everything within the repo

# Create the virtual env
if ! [ -d $REPO_ROOT/venv ]; then
	python -m venv $REPO_ROOT/venv
fi
. $REPO_ROOT/venv/bin/activate
pip install --upgrade pip
pip install -r $REPO_ROOT/requirements.txt
# Create/delete the BUILD_DIR
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR
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
. ./beeswarm/bee-setup.sh

# Output the cloud config
beeswarm.py cfg --cloud-conf > $CLOUD_CONF
