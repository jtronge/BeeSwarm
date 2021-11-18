#!/bin/sh
# Untar and run the code tarball

TARBALL=$1
shift 1
# Untar the code tarball
tar -xvf $TARBALL
echo $@
# Exec the command
exec $@
