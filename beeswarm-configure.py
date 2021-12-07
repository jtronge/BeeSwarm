#!/usr/bin/env python3
"""Initial configuration script for BeeSwarm."""
import yaml
import os
import re
import sys


# Most secrets are stored in the SECRETS environment variable
secrets = yaml.load(os.getenv('SECRETS'))


def get_secret(key):
    """Get a secret from the environment."""
    # First check in the SECRETS environment variable
    if key in secrets:
        return secrets[key]
    # Otherwise just return the result of os.getenv()
    return os.getenv(key)


def sub_env_vars(conf):
    """Substitute all environment variables in the configuration."""
    # This could probably be more Pythonic
    if type(conf) is dict:
        return {key: sub_env_vars(conf[key]) for key in conf}
    elif type(conf) is list:
        return [sub_env_vars(elm) for elm in conf]
    # Base case
    if type(conf) is not str:
        return conf
    regex = r'\$\{(.+)\}'
    m = re.search(regex, conf)
    if m is not None:
        key = m.groups()[0]
        # Return the substitution if there is one
        val = get_secret(key)
        if val is not None:
            return re.sub(regex, val, conf)
    return conf


with open('beeswarm.yml') as fp:
    conf = yaml.load(fp, Loader=yaml.CLoader)

# Replace all entries that match ${} with corresponding environment variables
conf = sub_env_vars(conf)
yaml.dump(conf, sys.stdout)

# Generate the beeswarm.conf
beeswarm_conf = []
for key in ['bee_branch', 'ctr_archive', 'wfm_port', 'tm_port']:
    beeswarm_conf.append('{}={}\n'.format(key.upper(), conf[key]))
print(''.join(beeswarm_conf))

# Generate the beecloud config
with open(conf['bee_cloud_conf_fname'], 'w') as fp:
    yaml.dump(conf['bee_cloud_conf'], fp)
