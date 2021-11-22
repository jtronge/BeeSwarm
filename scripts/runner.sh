#!/bin/sh
OUTPUT=$1
shift
exec $@ > $OUTPUT 2>&1
