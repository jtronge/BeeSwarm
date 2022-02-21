## BeeSwarm

BeeSwarm is designed as a CI scalability and performance testing tool based on
the Build and Execute Environment (BEE) orchestration system. This repository
contains a number of test results for different publications. I've tried to add
git tags that reference each version of BeeSwarm and the particular tests that
were run. The `graphs` branch contains most of the results data as well as the
matplotlib code for generating the graphs. The `results` branch is more of a
staging branch that is used directly from CI for committing results to the
repository. Once results are pushed to that branch, I normally copy them over to
the `graphs` branch and then generate graph output from there, since I don't
want the CI code to accidentally clobber older results.
