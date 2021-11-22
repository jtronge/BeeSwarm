#!/bin/sh
# Untar and run the code tarball

TARBALL=$1
OUT_FILE=$2
ARGS="$3"
NAME=`echo $TARBALL | rev | cut -d'.' -f2- | rev`
# Untar the code tarball
tar -xvf $TARBALL
cd $NAME
exec ./run.sh $OUT_FILE "$ARGS"
