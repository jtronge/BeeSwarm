"""BeeSwarm graphing functions."""
import json
import numpy as np

def parse_runtime(path):
    """Parse a runtime from a workflow profile."""
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
    return complete_time - start_time

def compute_average_error(results):
    """Compute the average value and the error from a matrix of results."""
    average = np.average(results, 1)
    lower_error = average - np.amin(results, 1)
    upper_error = np.amax(results, 1) - average
    return average, [lower_error, upper_error]
