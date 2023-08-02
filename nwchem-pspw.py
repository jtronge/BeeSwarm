import json
import beeswarm_graph
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('./matplotlib-styles/paper.mplstyle')

commits = [
    'f29685d',
    '05aafc8',
    'adab52a',
    '519b710',
]
#inputs = [
#    'results/pspw/nwchem-pspw-05aafc8--0.json',
#    'results/pspw/nwchem-pspw-05aafc8--1.json',
#    'results/pspw/nwchem-pspw-519b710--0.json',
#    'results/pspw/nwchem-pspw-519b710--1.json',
#    'results/pspw/nwchem-pspw-adab52a--0.json',
#    'results/pspw/nwchem-pspw-adab52a--1.json',
#    'results/pspw/nwchem-pspw-f29685d--0.json',
#    'results/pspw/nwchem-pspw-f29685d--1.json',
#]
# calculate the average runtimes
times = []
all_times = []
for commit in commits:
    print('commit:', commit)
    total = 0.0
    commit_times = []
    for i in range(2):
        path = 'results/pspw/nwchem-pspw-{}--{}.json'.format(commit, i)
        runtime = beeswarm_graph.parse_runtime(path)
        print(runtime)
        commit_times.append(runtime)
        total += runtime
    all_times.append(commit_times)
    # add the average time
    times.append(total / 2.0)

# Compute the error
times = np.array(times)
all_times = np.array(all_times)
# times_min = np.amin(all_times, 1)
# times_max = np.amax(all_times, 1)
# [lower_error, upper_error]
# error = [times - times_min, times_max - times]
times, error = beeswarm_graph.compute_average_error(all_times)

fig, ax = plt.subplots()
ax.errorbar(commits, times, yerr=error, marker='o')
ax.set_ylabel('Execution time (s)')
ax.set_xlabel('NWChem commits')
plt.show()
