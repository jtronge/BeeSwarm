"""Special client for interacting with BEE in a CI environment."""
import argparse
import sys
import os
import subprocess
import time
import requests
import shutil


PORT = 5005


def launch(argv):
    """Launch a command in a subprocess."""
    pid = os.fork()
    if pid == 0:
        os.execv(shutil.which(argv[0]), argv)
    return pid


class BEEManager:
    """Class for starting and managing the BEE components."""

    def __init__(self, wfm_port):
        """BEE manager constructor."""
        self.wfm_port = wfm_port
        self.sched = None
        self.wfm = None
        self.tm = None

    def start(self):
        """Start all the components."""
        self.sched = launch(['python', '-m', 'beeflow.scheduler.scheduler'])
        time.sleep(3)
        self.wfm = launch(['python', '-m', 'beeflow.wf_manager'])
        self.tm = launch(['python', '-m', 'beeflow.task_manager'])
        time.sleep(3)

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
        assert resp.ok
        wf_id = resp.json()['wf_id']

        # Now start it
        resp = requests.post(url + wf_id, json={'wf_id': wf_id})
        assert resp.ok

        # Now poll the WFM until the workflow is done
        # TODO: There should be a better way to do this
        time.sleep(20)


def main(argv):
    parser = argparse.ArgumentParser(description='BEE CI client program')
    parser.add_argument('wfm_port', help='Workflow Manager Port')
    args = parser.parse_args(argv)

    bee = BEEManager(wfm_port=args.wfm_port)
    bee.start()

    bee.run_workflow('clamr-wf.tgz', 'clamr_wf.cwl', 'clamr_job.yml')
    # Now start workflows as configured
    pass


if __name__ == '__main__':
    main(sys.argv)
