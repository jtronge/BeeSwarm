import matplotlib.pyplot as plt
import json
import os


def compute_runtime(data):
    """Compute the runtime from profiling data."""
    start_time = None
    end_time = None
    for state in data['state_changes']:
        if state['next_state'] == 'RUNNING':
            start_time = state['timestamp']
        if state['next_state'] == 'COMPLETED':
            end_time = state['timestamp']
    return end_time - start_time


# hashes of NWChem commits that were tested
hashes = [
    '05aafc8',
    '519b710',
    'adab52a',
    'f29685d',
]
# process results for each commit hash
dirname = os.path.join('results', 'nwchem-scf')
runtimes = []
for h in hashes:
    # 4 tests were done for stability
    times = []
    for i in range(4):
        fname = os.path.join(dirname, 'nwchem-scf-{}--{}.json'.format(h, i))
        with open(fname) as fp:
            data = json.load(fp)
        time = compute_runtime(data)
        times.append(time)
    runtime = sum(times) / len(times)
    print('total runtime for', h, '=', runtime)
    runtimes.append(runtime)

fig, ax = plt.subplots()
ax.plot(hashes, runtimes)
ax.set_ylabel('Execution time (s)')
ax.set_xlabel('NWChem commits')
ax.set_title('NWChem Scaling Test - 4 Nodes')
plt.show()
