#!/bin/sh

REPO_ROOT=`pwd`

# Set up BEE
# . ./bee-setup.sh

# Build the container
cd $REPO_ROOT/containers/lulesh
ch-image build --force -t lulesh .

cd $REPO_ROOT/containers/beeswarm
ch-image build --force -t beeswarm .
ch-builder2tar beeswarm .
ch-tar2dir beeswarm.tar.gz .
ch-run beeswarm -- cat /etc/release

# Generate workflow
# TODO

# Run workflow with ci-client.py
# TODO

# Save results
# TODO
