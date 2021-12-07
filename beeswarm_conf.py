#!/usr/bin/env python3
"""Initial configuration script for BeeSwarm."""
import yaml
import json
import os
import re
import sys
import string


# Load the main beeswarm config file
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'beeswarm.yml')) as fp:
    conf = yaml.load(fp, Loader=yaml.CLoader)
# Load the BeeSwarm configuration secrets from the JSON-encoded secrets variable
secrets = os.getenv('SECRETS_JSON')
# Update the configuration
conf.update(json.loads(secrets))


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
    if val is not None:
        tmpl = string.Template(val)
        # Replace environment strings if we can
        return tmpl.safe_substitute(**os.environ)
    return None


if __name__ == '__main__':
    assert len(sys.argv) == 2
    key = sys.argv[1]
    val = resolve_key(key)
    if val is not None:
        print(val)
