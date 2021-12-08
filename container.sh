#!/bin/sh
CWD=`pwd`

ch-tar2dir $CWD/bee.tar.gz /tmp
ch-run --cd $CWD -b /var/tmp /tmp/bee /bin/bash
