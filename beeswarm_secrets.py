#!/usr/bin/env python3
"""Use the GitHub API to update secrets for the repository."""
import yaml
import json
from base64 import b64encode
# import nacl
from nacl import encoding, public
import requests
import os
import sys
import time


API_DOMAIN = 'api.github.com'


print('Updating secrets...', end='', flush=True)

# Load the main beeswarm config file
with open('beeswarm.yml') as fp:
    conf = yaml.load(fp, Loader=yaml.CLoader)
# Load the secrets yml file (this should not be kept in git)
with open('secrets.yml') as fp:
    secrets = yaml.load(fp, Loader=yaml.CLoader)

# Load the GitHub authentication from the secrets file
github_user = secrets['github_user'] if 'github_user' in secrets else None
github_pat = secrets['github_pat'] if 'github_pat' in secrets else None
if github_user is None or github_pat is None:
    sys.exit('`github_user` and `github_pat` are required to be set in the `secrets.yml` file')

owner = conf['beeswarm_repo_owner']
repo = conf['beeswarm_repo']

# Get the secret key for the repo
resp = requests.get(f'https://{API_DOMAIN}/repos/{owner}/{repo}/actions/secrets/public-key',
                    auth=(github_user, github_pat))
data = resp.json()
repo_key_id = data['key_id']
repo_pubkey = data['key']

# Update the SECRETS_JSON value
val = json.dumps(secrets)
# Encode the value
pubkey = public.PublicKey(repo_pubkey.encode('utf-8'), encoding.Base64Encoder())
sb = public.SealedBox(pubkey)
enc = sb.encrypt(val.encode('utf-8'))
enc_val = b64encode(enc).decode('utf-8')
resp = requests.put(f'https://{API_DOMAIN}/repos/{owner}/{repo}/actions/secrets/SECRETS_JSON',
                    auth=(github_user, github_pat),
                    json={'encrypted_value': enc_val, 'key_id': repo_key_id})
print('done')
