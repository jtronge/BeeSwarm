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
import json
import string


def launch(argv):
    """Launch a command in a subprocess."""
    pid = os.fork()
    if pid == 0:
        os.execv(shutil.which(argv[0]), argv)
    return pid


class BEEManager:
    """Class for starting and managing the BEE components."""

    def __init__(self, **kwargs):
        """BEE manager constructor."""
        self.wfm_port = conf['wfm_port']
        self.sched = None
        self.wfm = None
        # self.tm = None

    def start(self):
        """Start all the components."""
        self.sched = launch(['python', '-m', 'beeflow.scheduler.scheduler'])
        time.sleep(8)
        self.wfm = launch(['python', '-m', 'beeflow.wf_manager'])
        # self.tm = launch(['beeflow-cloud', '--tm', self.cloud_conf_path])
        # self.tm = launch(['python', '-m', 'beeflow.task_manager'])
        time.sleep(10)

    def run_workflow(self, name, workflow_path, main_cwl, yaml):
        """Execute a workflow."""
        base_url = 'http://127.0.0.1:{}'.format(self.wfm_port)
        url = '{}/{}/'.format(base_url, 'bee_wfm/v1/jobs')
        files = {
            'wf_name': name.encode(),
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
        # time.sleep(256)
        status_url = '{}/bee_wfm/v1/status/{}'.format(base_url, wf_id)
        resp = requests.get(status_url)
        status = resp.json()
        while not status['complete']:
            time.sleep(4)
            resp = requests.get(status_url)
            status = resp.json()

    def shutdown(self):
        """Shutdown and cleanup BEE (there should be a better way to do this)."""
        # Kill the GDB
        subprocess.run(['pkill', 'java'])
        # for pid in [self.sched, self.wfm, self.tm]:
        for pid in [self.sched, self.wfm]:
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


class ContainerError(Exception):
    """Container error class."""

    def __init__(self, msg):
        """Container error class constructor."""
        self.msg = msg


class Container:
    """Container class around Charliecloud interface."""

    def __init__(self, ctx_dir, name):
        """Container constructor."""
        self.ctx_dir = ctx_dir
        self.name = name
        self._build_complete = False

    def build(self, **build_args):
        """Build the container."""
        cmd = ['ch-image', 'build', '--force', '-t', self.name]
        for arg in build_args:
            cmd.append('--build-arg')
            cmd.append('{}={}'.format(arg, build_args[arg]))
        cmd.append('.')
        print('Running command:', ' '.join(cmd))
        # Run the build in the context dir
        cp = subprocess.run(cmd, cwd=self.ctx_dir)
        if cp.returncode != 0:
            raise ContainerError('Charliecloud build of container {} failed'.format(self.name))
        self._build_complete = True

    def push(self, remote):
        """Push the container up to a remote registry."""
        if not self._build_complete:
            raise ContainerError('Cannot push {}, no build has been done'.format(self.name))
        cp = subprocess.run('ch-image push {} {}'.format(self.name, remote).split())
        if cp.returncode != 0:
            raise ContainerError('Failed to push container {}'.format(self.name))


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


def expand_package_workflow(wfl_path, params, template_files, yml_data):
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

    # Dump the yaml input file
    yml_file = 'input.yml'
    fname = os.path.join(tmp_wfl_path, yml_file)
    with open(fname, 'w') as fp:
        yaml.dump(yml_data, fp)

    # Tar it up
    tarball = '{}.tgz'.format('rendered-wfl')
    print('Saving workflow tarball to', tarball)
    cmd = 'tar -C {} -czf {} {}'.format(TMPDIR, tarball, basename)
    subprocess.run(cmd.split())
    return tarball, yml_file


def scale_tests(args):
    """Run the configured scale tests."""
    parser = argparse.ArgumentParser(description='run configured scale tests')
    # parser.add_argument('--cloud-conf-path', required=True, help='path to cloud config file')
    args = parser.parse_args(args)

    # Start running BEE
    # bee = BEEManager(cloud_conf_path=args.cloud_conf_path)
    bee = BEEManager()
    bee.start()

    # Run each scale test as configured
    for test in conf['scale_tests']:
        # Build and push the container
        ctx_dir = test['container']['ctx_dir']
        name = test['container']['name']
        ctr = Container(ctx_dir, name)
        ctr.build(**test['container']['build_args'])
        # build_container(ctx_dir, name, remote)
        if 'remote' in test['container']:
            ctr.push(test['container']['remote'])

        # Expand and generate the workflow
        wfl_dir = test['wfl_dir']
        params = test['params']
        template_files = test['template_files']
        # Note 'inputs' used to be called 'yaml'
        yml_data = test['inputs']
        wfl_tarball, yml_file = expand_package_workflow(wfl_dir, params, template_files, yml_data)

        # Run the workflow
        wfl_name = test['name']
        main_cwl = test['main_cwl']
        bee.run_workflow(wfl_name, wfl_tarball, main_cwl, yml_file)

        # Save results
        # TODO: for now this is done by git in the outer script

    bee.shutdown()


def sub_env(param):
    """Substitute the environment into the configuration values."""
    # This could probably be more Pythonic
    if type(param) is dict:
        return {key: sub_env(param[key]) for key in param}
    elif type(param) is list:
        return [sub_env(elm) for elm in param]

    if type(param) is not str:
        return param

    tmpl = string.Template(param)
    return tmpl.safe_substitute(**os.environ)


def resolve_key(key):
    """Resolve a BeeSwarm configuration key value (or None)."""
    keys = key.split('.')
    val = conf
    for key in keys:
        try:
            try:
                val = val[int(key)]
            except ValueError:
                val = val[key]
        except KeyError:
            val = None
            break
    return val


def cfg(args):
    """BeeSwarm configuration management."""
    parser = argparse.ArgumentParser(description='beeswarm configuration tool')
    parser.add_argument('-k', '--key', help='get config value')
    parser.add_argument('--cloud-conf', action='store_true', help='output cloud config')
    args = parser.parse_args(args)
    if args.key is not None:
        val = resolve_key(args.key)
        if val is not None:
            print(val)

    # Dump the cloud launcher config
    if args.cloud_conf:
        cfg = conf['cloud_launcher_conf']
        yaml.dump(cfg, sys.stdout)


commands = {
    'scale-tests': scale_tests,
    'cfg': cfg,
}


def usage():
    """Print usage information."""
    print('usage:', sys.argv[0], '[command] [opts]...', file=sys.stderr)
    print('', file=sys.stderr)
    print('commands:', file=sys.stderr)
    for cmd in commands:
       print('{} -- {}'.format(cmd, commands[cmd].__doc__), file=sys.stderr)
    sys.exit(1)


def main():
    """Main launch function."""
    if len(sys.argv) < 2:
        usage()
    cmd = sys.argv[1]
    if cmd.startswith('-'):
        usage()
    if cmd not in commands:
        print('invalid cmd', cmd, file=sys.stderr)
        usage()
    commands[cmd](sys.argv[2:])


# Load the main beeswarm config file
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'beeswarm.yml')) as fp:
    conf = yaml.load(fp, Loader=yaml.CLoader)
# Load the BeeSwarm configuration secrets from the JSON-encoded secrets variable
secrets = os.getenv('SECRETS_JSON')
# Update the configuration
conf.update(json.loads(secrets))
conf = sub_env(conf)


if __name__ == '__main__':
    main()
