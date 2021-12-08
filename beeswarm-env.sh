#!/bin/sh
# Set up the BeeSwarm environment for local development
# NOTE: This has to be in sync with the environment variables set in
# beeswarm.sh

# Set the secrets value to the JSON-encoded contents of 'secrets.yml'
export SECRETS_JSON=`python3 -c "import yaml; import json; print(json.dumps(yaml.load(open('secrets.yml'), Loader=yaml.CLoader)))"`
export CH_IMAGE_USERNAME=`python3 -c "import yaml; print(yaml.load(open('secrets.yml'), Loader=yaml.CLoader)['ch_image_username'])"`
export CH_IMAGE_PASSWORD=`python3 -c "import yaml; print(yaml.load(open('secrets.yml'), Loader=yaml.CLoader)['ch_image_password'])"`
export REPO_ROOT=`pwd`

if [ -d venv ]; then
	. ./venv/bin/activate
fi
