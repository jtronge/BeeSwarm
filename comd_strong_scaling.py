import matplotlib.pyplot as plt
import json


profiles = [
    ('results/comd-2021-12-10/comd-1.json', 1),
    ('results/comd-2021-12-10/comd-2.json', 2),
    ('results/comd-2021-12-10/comd-4.json', 4),
    ('results/comd-2021-12-10/comd-8.json', 8),
    ('results/comd-2021-12-10/comd-16.json', 16),
]

# Make sure the profiles are sorted
profiles.sort(key=lambda t: t[1])
results = []
for profile in profiles:
    fname = profile[0]
    procs = profile[1]
    with open(fname) as fp:
        data = json.load(fp)
    # Determine the start time and the end time from the profile data
    run_times = []
    complete_times = []
    for state in data['state_changes']:
        if state['next_state'] == 'RUNNING':
            run_times.append(state['timestamp'])
        if state['next_state'] == 'COMPLETED':
            complete_times.append(state['timestamp'])
    start = min(run_times)
    finish = max(complete_times)
    runtime = finish - start
    print('For', procs, 'cores the total time was', runtime, 'seconds')
    results.append((procs, runtime))

# Use a string for the process count to use categorical plotting
proc_counts = [str(res[0]) for res in results]
runtimes = [res[1] for res in results]

fig, ax = plt.subplots()
ax.plot(proc_counts, runtimes)
ax.set_ylabel('Execution time (s)')
ax.set_xlabel('Process counts')
ax.set_title('CoMD Strong Scaling Test (n1-standard-16)')
plt.show()
