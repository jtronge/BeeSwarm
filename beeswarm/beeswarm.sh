#!/bin/sh
# Workflow init script

. ./beeswarm/env.sh
. ./beeswarm/init.sh

# Set up the cloud
beeflow-cloud --setup $CLOUD_CONF
# Wait for set up completion
sleep 300
beeflow-cloud --connect $CLOUD_CONF
beeswarm.py scale-tests # --cloud-conf-path $CLOUD_CONF

# Upon completion of the scale tests, commit all results to the `results` branch
# in the results folder
git fetch
git checkout results
RESULTS_DIR=results/`beeswarm.py cfg -k test_name`
mkdir -p $RESULTS_DIR
cp `beeswarm.py cfg -k time_log` $RESULTS_DIR
cp ~/.beeflow/*.json $RESULTS_DIR
git add $RESULTS_DIR
git commit -am "BeeSwarm test results: `date +%F_%T`"
git push -u origin results
