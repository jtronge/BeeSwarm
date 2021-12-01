#!/bin/sh

# Set up BEE
. ./bee-setup.sh

# Build the container
cd containers/lulesh
ch-image build --force -t lulesh .

# Generate workflow
# TODO

# Run workflow with ci-client.py
# TODO

# Save results
# TODO
