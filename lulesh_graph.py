import json
import os
import matplotlib.pyplot as plt


def parse_lulesh_output(lines):
    """Parse the LULESH stdout."""
    lines = [line.strip() for line in lines]
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


files = [
    'results/lulesh-results/lulesh-1ca67244-0492-454c-b052-3db81d85fc83/lulesh-1ca67244-0492-454c-b052-3db81d85fc83.out',
    'results/lulesh-results/lulesh-cc3fde5d-9a0f-4c0a-9b54-176aa3f3f98a/lulesh-cc3fde5d-9a0f-4c0a-9b54-176aa3f3f98a.out',
    'results/lulesh-results/lulesh-ded72496-bdde-4411-8ee4-6c44f3fe68c1/lulesh-ded72496-bdde-4411-8ee4-6c44f3fe68c1.out',
    'results/lulesh-results/lulesh-ee96ace8-6bbe-425b-a546-e3da4b5010f8/lulesh-ee96ace8-6bbe-425b-a546-e3da4b5010f8.out',
]

results = []
for file_ in files:
    with open(file_) as fp:
        results.append(parse_lulesh_output(fp.readlines()))

results.sort(key=lambda res: res['mpi_tasks'])

foms = [res['fom'] for res in results]
mpi_tasks = [str(res['mpi_tasks']) for res in results]
fig, ax = plt.subplots()
ax.plot(mpi_tasks, foms, marker='o')
ax.set_ylabel('FOM (z/s)')
# Note: distributed across 2 n1-standard-32 nodes
ax.set_xlabel('MPI tasks')
# ax.set_title('LULESH Scaling Test (n1-standard-32)')
plt.show()
