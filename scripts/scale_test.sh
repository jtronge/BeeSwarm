#!/bin/sh
# Untar and run the code tarball

# TODO: Figure out a way to output the test results/pipe stdin/stdout to a
# result file for processing (perhaps using dup2)
TARBALL=$1
shift 1
# Untar the code tarball
tar -xvf $TARBALL
# Exec the command
exec $@
