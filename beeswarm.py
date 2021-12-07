#!/usr/bin/env python3
"""BeeSwarm main script."""
import subprocess
import argparse
import sys
import os
import time
import requests
import shutil
import jinja2
import yaml
# from beeflow import cloud_launcher


def launch(argv):
    """Launch a command in a subprocess."""
    pid = os.fork()
    if pid == 0:
        os.execv(shutil.which(argv[0]), argv)
    return pid


class BEEManager:
    """Class for starting and managing the BEE components."""

    def __init__(self, wfm_port, bee_cloud_conf, bee_cloud_conf_fname, **kwargs):
        """BEE manager constructor."""
        self.wfm_port = wfm_port
        self.bee_cloud_conf = bee_cloud_conf
        self.bee_cloud_conf_fname = bee_cloud_conf_fname
        self.sched = None
        self.wfm = None
        self.tm = None

    def start(self):
        """Start all the components."""
        self.sched = launch(['python', '-m', 'beeflow.scheduler.scheduler'])
        time.sleep(8)
        self.wfm = launch(['python', '-m', 'beeflow.wf_manager'])
        self.tm = launch(['beeflow-cloud', '--tm', self.bee_cloud_conf_fname])
        # self.tm = launch(['python', '-m', 'beeflow.task_manager'])
        time.sleep(8)

    def run_workflow(self, workflow_path, main_cwl, yaml):
        """Execute a workflow."""
        url = 'http://127.0.0.1:{}/{}/'.format(self.wfm_port, 'bee_wfm/v1/jobs')
        files = {
            'wf_name': 'test'.encode(),
            'wf_filename': 'some_wfl.tgz',
            'workflow': open(workflow_path, 'rb'),
            'main_cwl': main_cwl, 
            'yaml': yaml,
        }
        resp = requests.post(url, files=files)
        if not resp.ok:
            print('WFM request failed', file=sys.stderr)
            print(resp.text, file=sys.stderr)
            sys.exit(1)
        wf_id = resp.json()['wf_id']

        # Now start it
        resp = requests.post(url + wf_id, json={'wf_id': wf_id})
        if not resp.ok:
            print('WFM request failed', file=sys.stderr)
            print(resp.text, file=sys.stderr)
            sys.exit(1)

        # Now wait until the workflow is complete (there should be a better way
        # to do this)
        time.sleep(256)

    def shutdown(self):
        """Shutdown and cleanup BEE (there should be a better way to do this)."""
        # Kill the GDB
        subprocess.run(['pkill', 'java'])
        for pid in [self.sched, self.wfm, self.tm]:
            subprocess.run(['kill', str(pid)])


"""
def main(argv):
    parser = argparse.ArgumentParser(description='BEE CI client program')
    parser.add_argument('wfm_port', help='Workflow Manager Port')
    args = parser.parse_args(argv)

    bee = BEEManager(wfm_port=args.wfm_port)
    bee.start()
    bee.run_workflow('clamr-wf.tgz', 'clamr_wf.cwl', 'clamr_job.yml')
    bee.shutdown()
"""


def build_container(ctx_dir, name, remote=None):
    """Build and push a container with Charliecloud."""

    def run(cmd):
        """Run a command with subprocess."""
        return subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #return subprocess.run(cmd.split())

    cwd = os.getcwd()
    os.chdir(ctx_dir)
    print('Building container', name)
    cp = run('ch-image build --force -t {} .'.format(name))
    assert cp.returncode == 0
    if remote is not None:
        print('Pushing container', name, 'to', remote)
        cp = run('ch-image push {} {}'.format(name, remote))
        assert cp.returncode == 0
    os.chdir(cwd)


def prepare_workflow(loc):
    """Prepare a workflow by creating a tarball."""
    dirname = os.path.dirname(loc)
    basename = os.path.basename(loc)
    tarball = '{}.tgz'.format(basename)
    cmd = 'tar -C {} -czf {} {}'.format(dirname, tarball, basename)
    cp = subprocess.run(cmd.split())
    if cp.returncode != 0:
        raise RuntimeError('Packaging failed')
    return tarball


TMPDIR = '/tmp'


def expand_package_workflow(wfl_path, params, template_files):
    """Expand a workflow and put in a tarball to be submitted to BEE."""
    # tmp_wfl_path = '/tmp/{}'.format(int(time.time()))
    # TODO: Use tempfile.mkdtemp() here 
    basename = str(int(time.time()))
    tmp_wfl_path = os.path.join(TMPDIR, basename)
    shutil.rmtree(tmp_wfl_path, ignore_errors=True)
    shutil.copytree(wfl_path, tmp_wfl_path)

    # Render each template file with jinja2
    print('Rendering templated workflow in', tmp_wfl_path)
    for f in template_files:
        f = os.path.join(tmp_wfl_path, f)
        with open(f) as fp:
            tmpl = jinja2.Template(fp.read())
        with open(f, 'w') as fp:
            fp.write(tmpl.render(**params))

    tarball = '{}.tgz'.format('rendered-wfl')
    print('Saving workflow tarball to', tarball)
    cmd = 'tar -C {} -czf {} {}'.format(TMPDIR, tarball, basename)
    subprocess.run(cmd.split())
    return tarball


def main():
    with open('beeswarm.yml') as fp:
        conf = yaml.load(fp, Loader=yaml.CLoader)

    bee = BEEManager(**conf)
    bee.start()

    for test in conf['scale_tests']:
        ctx_dir = test['container']['ctx_dir']
        name = test['container']['name']
        remote = test['container']['remote']
        # build_container('containers/lulesh', 'lulesh:newest', 'jtronge/lulesh:newest')
        build_container(ctx_dir, name, remote)

        # Expand and generate the workflow
        wfl_dir = test['wfl_dir']
        params = test['params']
        template_files = test['template_files']
        #wfl_dir = './workflows/lulesh'
        #params = {'container': 'jtronge/lulesh:newest'}
        #template_files = ['lulesh.cwl']
        wfl_tarball = expand_package_workflow(wfl_dir, params, template_files)

        main_cwl = test['main_cwl']
        yml_file = test['yaml']
        #main_cwl = 'lulesh.cwl'
        #yaml = 'lulesh.yml'
        # Submit the workflow
        bee.run_workflow(wfl_tarball, main_cwl, yml_file)

    bee.shutdown()


if __name__ == '__main__':
    main()
