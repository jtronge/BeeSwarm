import json
import os


#fname = 'results/lulesh-1-core.json'
#with open(fname) as fp:
#    profile = json.load(fp)
#task_id = profile['state_changes'][0]['task_id']

fname = 'results/af961ba0-aa2e-483c-8869-806ef0d94b54_2121f0ad-5000-4ae2-bcfc-28c395827879_1639700420.json'
with open(fname) as fp:
    data = json.load(fp)
stdout = None
for key in data:
    if key.endswith('.out'):
        stdout = data[key]


def parse_lulesh_output(content):
    """Parse the LULESH stdout."""
    lines = [line.strip() for line in content.split('\n')]
    lines = [line for line in lines if line]
    # Get the fom value
    fom = None
    mpi_tasks = None
    for line in lines:
        parts = [part.strip() for part in line.split('=')]
        if parts[0] == 'FOM':
            fom = float(parts[1].split()[0])
        if parts[0] == 'MPI tasks':
            mpi_tasks = int(parts[1])
    print('FOM value:', fom)
    print('MPI tasks:', mpi_tasks)
    return {
        'fom': fom,
        'mpi_tasks': mpi_tasks
    }


print(parse_lulesh_output(stdout))
