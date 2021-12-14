#!/bin/sh
# Workflow init script

. ./beeswarm/env.sh
. ./beeswarm/init.sh

#CLOUD_CONFIG=`beeswarm.py cfg -k cloud_config_path`
# pytho -m beeflow.task_manager &
#beeflow-cloud --tm $CLOUD_CONFIG &
# Set up the cloud
beeflow-cloud --setup $CLOUD_CONF
# Wait for set up completion
sleep 300
beeflow-cloud --connect $CLOUD_CONF
beeswarm.py scale-tests # --cloud-conf-path $CLOUD_CONF

# Launch the BeeSwarm Python script
# ./beeswarm.py $WFM_PORT

# cat ~/.beeflow/*.json

# Upon completion of the scale tests, commit all results to the `results` branch
# in the results folder
git fetch
git checkout results
mkdir -p results/
cp ~/.beeflow/*.json results/
git add results
git commit -am "BeeSwarm test results: `date +%F_%T`"
git push -u origin results
