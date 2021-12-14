import matplotlib.pyplot as plt
import json


profiles = (
    (1, 4, 'results/comd-2021-12-14/comd-1-node-4-cores.json'),
    (2, 8, 'results/comd-2021-12-14/comd-2-nodes-8-cores.json'),
    (4, 16, 'results/comd-2021-12-14/comd-4-nodes-16-cores.json'),
)

y_axis = []
x_axis = []
for profile in profiles:
    # Add labels to the x axis
    x_axis.append('{} nodes ({} cores)'.format(profile[0], profile[1]))
    with open(profile[2]) as fp:
        data = json.load(fp)
    run_times = []
    complete_times = []
    for state in data['state_changes']:
        if state['next_state'] == 'RUNNING':
            run_times.append(state['timestamp'])
        if state['next_state'] == 'COMPLETED':
            complete_times.append(state['timestamp'])
    # for state in profile[]
    start_time = min(run_times)
    finish_time = max(complete_times)
    runtime = finish_time - start_time
    # Add times to y_axis
    y_axis.append(runtime)
    print('Total runtime for "{}": {}'.format(profile[2], runtime))

fig, ax = plt.subplots()
ax.plot(x_axis, y_axis)
ax.set_ylabel('Execution time (s)')
ax.set_title('CoMD Strong Scaling Test - Multiple Nodes (n1-standard-4)')
plt.show()
