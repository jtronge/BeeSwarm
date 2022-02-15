"""Simple script to find recent profile files."""
import sys
import json
import time


now = int(time.time())
for file in sys.argv[1:]:
    with open(file) as fp:
        data = json.load(fp)
    t = min(state['timestamp'] for state in data['state_changes'])
    if (now - t) < (60 * 60 * 4):
        print(file)
