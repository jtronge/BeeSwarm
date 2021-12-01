#!/bin/sh
IMAGE_REF=$1
SCRIPT=$2
shift 2
ARGS="$@"

ch-image pull $IMAGE_REF
ch-builder2tar -b ch-image $IMAGE_REF .
ch-tar2dir $IMAGE_REF .
CONTAINER_DIR=`echo $IMAGE_REF | tr '/' '%'`
exec ch-run $CONTAINER_DIR -- $SCRIPT $ARGS
