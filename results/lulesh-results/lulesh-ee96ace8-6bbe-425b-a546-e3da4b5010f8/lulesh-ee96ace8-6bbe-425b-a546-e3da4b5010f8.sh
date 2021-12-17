#! /bin/bash
#SBATCH --job-name=lulesh-ee96ace8-6bbe-425b-a546-e3da4b5010f8
#SBATCH --output=/home/bee/.beeflow/workflows/4c2f2441-b607-4990-bbe4-a226fc33a3e4/lulesh-ee96ace8-6bbe-425b-a546-e3da4b5010f8/lulesh-ee96ace8-6bbe-425b-a546-e3da4b5010f8.out
#SBATCH --error=/home/bee/.beeflow/workflows/4c2f2441-b607-4990-bbe4-a226fc33a3e4/lulesh-ee96ace8-6bbe-425b-a546-e3da4b5010f8/lulesh-ee96ace8-6bbe-425b-a546-e3da4b5010f8.err
#SBATCH -n 1
module load charliecloud

srun mkdir -p /tmp
srun ch-tar2dir /home/bee/container_archive/jtronge%lulesh:mpi-no-openmp.tar.gz /tmp
srun ch-run /tmp/jtronge%lulesh:mpi-no-openmp --cd /home/bee -- /lulesh2.0 -s 60 -i 600
srun rm -rf /tmp/jtronge%lulesh:mpi-no-openmp
