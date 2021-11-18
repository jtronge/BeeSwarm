#!/usr/bin/env python3
import subprocess
import shutil
import os
import sys
import uuid
import argparse


parser = argparse.ArgumentParser(description='scalability testing script')
parser.add_argument('--tarball', required=True)
parser.add_argument('--bin', required=True)
args = parser.parse_args()

# Untar the recently built program
subprocess.run(['tar', '-xvf', args.tarball])

# Execute the compiled program
cmd = args.bin.split()
os.execv(cmd[0], cmd)

# print(args.tarball)
# sys.exit(0)


TEST_DIR = '/tmp'
REPO = 'https://github.com/LLNL/LULESH.git'

with open('scale_test.json', 'w') as fp:
    fp.write('')
sys.exit(0)

repo_dir = os.path.join(TEST_DIR, str(uuid.uuid4()))
subprocess.run([
    'git',
    'clone',
    REPO,
    repo_dir,
])
os.chdir(repo_dir)
subprocess.run([
    'git',
    'checkout',
    '7bb829396f363dfb5c6897c21b6bfe571fcc2bf9',
])
try:
    os.mkdir('build')
except FileExistsError:
    pass
os.chdir('build')
mpicxx = shutil.which('mpicxx')
if mpicxx is None:
    sys.exit('Cannot find mpicxx compiler in path!')
subprocess.run([
    'cmake',
    '-DCMAKE_BUILD_TYPE=Release',
    '-DMPI_CXX_COMPILER={}'.format(mpicxx),
    '../',
])
subprocess.run(['make'])
subprocess.run(['./lulesh2.0', '-p'])
