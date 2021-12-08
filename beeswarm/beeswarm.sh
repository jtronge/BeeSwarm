#!/bin/sh
# Workflow init script

. ./beeswarm/env.sh
. ./beeswarm/init.sh

#CLOUD_CONFIG=`beeswarm.py cfg -k cloud_config_path`
# pytho -m beeflow.task_manager &
#beeflow-cloud --tm $CLOUD_CONFIG &
# beeswarm.py scale-tests --cloud-conf-path $CLOUD_CONF

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
