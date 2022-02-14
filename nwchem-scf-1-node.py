import os
import json

result_dir = 'results/nwchem-scf-1-node/'
commits = [
    'f29685d',
    '05aafc8',
    'adab52a',
    '519b710',
]
task_counts = [
    2,
    4,
    8,
    16,
]
for commit in commits:
    for tc in task_counts:
        for i in range(4):
            fname = 'nwchem-scf-{}-{}--{}'.format(commit, tc, i)
            path = os.path.join(result_dir, fname)
            print(path)
            print(os.path.exists(path))
