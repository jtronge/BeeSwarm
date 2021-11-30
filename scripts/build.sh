#!/bin/sh
CWD=`pwd`
BUILD_SCRIPT=$1

curl -L $BUILD_SCRIPT > /tmp/build.sh
chmod 755 /tmp/build.sh
exec /tmp/build.sh
