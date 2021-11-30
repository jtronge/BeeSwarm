#!/bin/sh
# Untar and run the code tarball

OUT_FILE=~/run-output.txt
BIN=$1
shift 1
ARGS="$@"

echo "$BIN $ARGS"
exec ./$BIN $ARGS > $OUT_FILE 2>&1
