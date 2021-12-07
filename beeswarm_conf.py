#!/usr/bin/env python3
"""Initial configuration script for BeeSwarm."""
import yaml
import json
import os
import re
import sys
import string
import argparse


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


# Load the main beeswarm config file
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'beeswarm.yml')) as fp:
    conf = yaml.load(fp, Loader=yaml.CLoader)
# Load the BeeSwarm configuration secrets from the JSON-encoded secrets variable
secrets = os.getenv('SECRETS_JSON')
# Update the configuration
conf.update(json.loads(secrets))
conf = sub_env(conf)


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='beeswarm configuration tool')
    parser.add_argument('-k', '--key', help='get config value')
    parser.add_argument('--cloud-conf', action='store_true', help='output cloud config')
    args = parser.parse_args()
    if args.key is not None:
        val = resolve_key(args.key)
        if val is not None:
            print(val)

    # Dump the cloud launcher config
    if args.cloud_conf:
        cfg = conf['cloud_launcher_conf']
        yaml.dump(cfg, sys.stdout)
