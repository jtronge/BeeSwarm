#! /bin/bash
#SBATCH --job-name=lulesh-cc3fde5d-9a0f-4c0a-9b54-176aa3f3f98a
#SBATCH --output=/home/bee/.beeflow/workflows/5ff22bc7-4e34-44c5-b446-92e735fe8609/lulesh-cc3fde5d-9a0f-4c0a-9b54-176aa3f3f98a/lulesh-cc3fde5d-9a0f-4c0a-9b54-176aa3f3f98a.out
#SBATCH --error=/home/bee/.beeflow/workflows/5ff22bc7-4e34-44c5-b446-92e735fe8609/lulesh-cc3fde5d-9a0f-4c0a-9b54-176aa3f3f98a/lulesh-cc3fde5d-9a0f-4c0a-9b54-176aa3f3f98a.err
#SBATCH -n 64
module load charliecloud

srun mkdir -p /tmp
srun ch-tar2dir /home/bee/container_archive/jtronge%lulesh:mpi-no-openmp.tar.gz /tmp
srun ch-run /tmp/jtronge%lulesh:mpi-no-openmp --cd /home/bee -- /lulesh2.0 -s 60 -i 600
srun rm -rf /tmp/jtronge%lulesh:mpi-no-openmp
