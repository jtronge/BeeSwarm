import matplotlib.pyplot as plt
import json

plt.style.use('./matplotlib-styles/paper.mplstyle')

files = [
    'results/nwchem-run-f29685d5bde59ac9c7f71b7ce6193720aaba1a8b.json',
    'results/nwchem-run-05aafc87223af82f58865d8b0f924dabd1adacbc.json',
    'results/nwchem-run-adab52acbbc0fb65b35856abf53937360bb52026.json',
    'results/nwchem-run-519b710bd09ebe3c10703293093d3cf70ce44333.json',
]
commits = []
times = []
for file in files:
    with open(file) as fp:
        data = json.load(fp)
    start_time = None
    end_time = None
    for state in data['state_changes']:
        if state['next_state'] == 'RUNNING':
            start_time = state['timestamp']
        if state['next_state'] == 'COMPLETED':
            end_time = state['timestamp']
    print('total time:', end_time - start_time)
    commit = file.split('.')[0].split('-')[2]
    # only show first 7 characters
    commits.append(commit[:7])
    times.append(end_time - start_time)

fig, ax = plt.subplots()
ax.plot(commits, times, marker='o')
ax.set_ylabel('Execution time (s)')
ax.set_xlabel('NWChem commits')
plt.show()
