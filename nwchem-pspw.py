import json
import beeswarm_graph
import matplotlib.pyplot as plt

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
for commit in commits:
    print('commit:', commit)
    total = 0.0
    for i in range(2):
        path = 'results/pspw/nwchem-pspw-{}--{}.json'.format(commit, i)
        runtime = beeswarm_graph.parse_runtime(path)
        print(runtime)
        total += runtime
    # add the average time
    times.append(total / 2.0)

fig, ax = plt.subplots()
ax.plot(commits, times, marker='o')
ax.set_ylabel('Execution time (s)')
ax.set_xlabel('NWChem commits')
plt.show()
