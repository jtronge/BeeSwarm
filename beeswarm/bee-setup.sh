#!/bin/sh
# Run the CI workflow, installing BEE and all dependencies
CWD=`pwd`

# Pull down the neo4j container
mkdir -p $HOME/img
ch-image pull neo4j:3.5.22
mkdir -p $REPO_ROOT/img
ch-builder2tar -b ch-image neo4j:3.5.22 $REPO_ROOT/img
mv $REPO_ROOT/img/neo4j* $REPO_ROOT/img/neo4j.tar.gz
GDB_IMG=$REPO_ROOT/img/neo4j.tar.gz

# Install BEE
cd $BUILD_DIR
git clone https://`beeswarm.py cfg -k github_pat`:x-oauth-basic@github.com/lanl/BEE_Private.git \
	-b `beeswarm.py cfg -k bee_branch` || exit 1
cd BEE_Private
# Set up the environment
# python3 -m venv venv
# . venv/bin/activate
# pip install --upgrade pip poetry
# We assume that the virtual env has been created at a higher level
pip install poetry
# Install with cloud_extras
poetry install -E cloud_extras

# Write a test config
rm -rf $HOME/.config/beeflow
mkdir -p $HOME/.config/beeflow
cat >> $HOME/.config/beeflow/bee.conf <<EOF
[DEFAULT]
bee_workdir = $HOME/.beeflow
workload_scheduler = Simple
use_archive = False

[task_manager]
listen_port = `beeswarm.py cfg -k tm_port`
container_runtime = Charliecloud

[charliecloud]
image_mntdir = /tmp
chrun_opts = --cd $HOME
container_dir = $HOME/img

[graphdb]
hostname = localhost
dbpass = `beeswarm.py cfg -k gdb_pass`
bolt_port = 7687
http_port = 7474
https_port = 7473
gdb_image = $GDB_IMG
gdb_image_mntdir = /tmp

[scheduler]
listen_port = 5600

[workflow_manager]
listen_port = `beeswarm.py cfg -k wfm_port`

[builder]
container_archive = `beeswarm.py cfg -k ctr_archive`
deployed_image_root = /tmp
container_output_path = /
container_type = charliecloud
EOF

cd $CWD
