import os
import string
import numpy as np
import matplotlib.pyplot as plt
import beeswarm_graph

plt.style.use('./matplotlib-styles/paper.mplstyle')

tmpl = string.Template(
    'results/nwchem-oniom2/nwchem-oniom2-$commit-$task_count--$run.json',
)
commits = [
    'f29685d',
    '05aafc8',
    'adab52a',
    '519b710',
]
task_counts = [
    '2',
    '4',
    '8',
    '16',
]
markers = [
    '.',
    '^',
    '8',
    's',
]

fig, ax = plt.subplots()
for i, commit in enumerate(commits):
    all_runtimes = []
    for task_count in task_counts:
        runtimes = []
        for run in range(0, 2):
            path = tmpl.substitute(commit=commit, task_count=task_count, run=run)
            print(path)
            runtime = beeswarm_graph.parse_runtime(path)
            runtimes.append(runtime)
        all_runtimes.append(runtimes)
    runtimes, error = beeswarm_graph.compute_average_error(np.array(all_runtimes))
    ax.errorbar(task_counts, runtimes, yerr=error, label=commit, marker=markers[i])
ax.set_ylabel('Execution time (s)')
ax.set_xlabel('MPI task counts')
ax.legend()
plt.show()
