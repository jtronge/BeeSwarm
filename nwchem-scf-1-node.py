"""Scaling test of NWChem with different numbers of MPI tasks for different committs."""
import os
import json
import matplotlib.pyplot as plt

plt.style.use('./matplotlib-styles/paper.mplstyle')

result_dir = 'results/nwchem-scf-1-node/'
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
    'o',
    's',
    '^',
    'X',
]

fig, ax = plt.subplots()
for i, commit in enumerate(commits):
    runtimes = []
    for tc in task_counts:
        runtime = 0.0
        for j in range(4):
            fname = 'nwchem-scf-{}-{}--{}.json'.format(commit, tc, j)
            path = os.path.join(result_dir, fname)
            with open(path) as fp:
                data = json.load(fp)
            start_times = []
            complete_times = []
            for state in data['state_changes']:
                if state['next_state'] == 'RUNNING':
                    start_times.append(state['timestamp'])
                if state['next_state'] == 'COMPLETED':
                    complete_times.append(state['timestamp'])
            start_time = min(start_times)
            complete_time = max(complete_times)
            runtime += (complete_time - start_time)
        runtime /= 4.0
        print('Runtime -', commit, '-', tc, 'tasks =>', runtime)
        runtimes.append(runtime)
    ax.plot(task_counts, runtimes, label=commit, marker=markers[i])
ax.set_ylabel('Execution time (s)')
ax.set_xlabel('MPI task counts')
ax.legend()
plt.show()
