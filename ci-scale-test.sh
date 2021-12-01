#!/bin/sh

# Set up BEE
. ./bee-setup.sh

# Build the container
cd containers/lulesh
ch-image build --force -t lulesh .
