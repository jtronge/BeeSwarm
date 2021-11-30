#!/bin/sh
# Untar and run the code tarball

BIN=$1
TARBALL=$2
OUT_FILE=$3
shift 3
ARGS="$@"

NAME=`echo $TARBALL | rev | cut -d'.' -f3- | rev`
# Untar the code tarball
tar -xvf $TARBALL
cd $NAME
echo "$BIN $ARGS"
exec ./$BIN $ARGS > $OUT_FILE 2>&1
