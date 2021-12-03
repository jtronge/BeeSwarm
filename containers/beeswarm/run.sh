#!/bin/sh
# Script to run a container based on an input parameter
IMAGE_REF=$1
OUT_DIR=$2
BIN=$3
CH_RUN_OPTS="--cd $HOME"
shift 3
ARGS="$@"

ch-image pull $IMAGE_REF
ch-builder2tar -b ch-image $IMAGE_REF $OUT_DIR
ch-tar2dir $IMAGE_REF $OUT_DIR
CONTAINER_DIR=`echo $IMAGE_REF | tr '/' '%'`
exec ch-run $CH_RUN_OPTS $OUT_DIR/$CONTAINER_DIR -- $BIN $ARGS
