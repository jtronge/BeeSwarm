# Running BeeSwarm Locally

To run BeeSwarm locally make sure that the two main configuration files are set
up:

* `beeswarm.yml`: general configuration values
* `secrets.yml`: secret values, such as auth codes and usernames that should not
  be commited

Once those are configured source `beeswarm-env.sh` to set up a CI-like
environment and then execute `./beeswarm.sh` to run BeeSwarm.

WARNING: Make sure that your `~/.config/beeflow/bee.conf` config file is backed
up. The BeeSwarm set up will overwrite it.
