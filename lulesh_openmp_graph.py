"""Graphing code for LULESH OpenMP results."""
import json
import os
import matplotlib.pyplot as plt


# List of (profile file, OpenMP thread count)
profiles = [
    ('lulesh-openmp-2-core.json', 2),
    ('lulesh-openmp-4-core.json', 4),
    ('lulesh-openmp-8-core.json', 8),
    ('lulesh-openmp-16-core.json', 16),
]
profile_dir = os.path.join('results', 'lulesh-openmp')
profiles = [(os.path.join(profile_dir, profile[0]), profile[1]) for profile in profiles]
data = []
for profile in profiles:
    with open(profile[0]) as fp:
        pdata = json.load(fp)
    data.append(pdata)

# Determine the total runtime based on the BEE profile data
times = []
for pdata in data:
    running = []
    completed = []
    for state_change in pdata['state_changes']:
        if state_change['next_state'] == 'RUNNING':
            running.append(state_change['timestamp'])
        if state_change['next_state'] == 'COMPLETED':
            completed.append(state_change['timestamp'])
    times.append(max(completed) - min(running))
    #max(completed)
    #min(running)
# Add the VM labels based on the number of threads used
vms = ['n1-standard-{}'.format(profile[1]) for profile in profiles]
fig, ax = plt.subplots()
ax.plot(vms, times)
ax.set_ylabel('Execution Time (s)')
ax.set_xlabel('Google Compute Engine VM Type')

plt.show()
