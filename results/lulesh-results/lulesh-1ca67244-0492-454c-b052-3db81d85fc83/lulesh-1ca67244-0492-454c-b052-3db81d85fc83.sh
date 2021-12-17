#! /bin/bash
#SBATCH --job-name=lulesh-1ca67244-0492-454c-b052-3db81d85fc83
#SBATCH --output=/home/bee/.beeflow/workflows/86456209-c01a-426c-bb39-be4065e93e4f/lulesh-1ca67244-0492-454c-b052-3db81d85fc83/lulesh-1ca67244-0492-454c-b052-3db81d85fc83.out
#SBATCH --error=/home/bee/.beeflow/workflows/86456209-c01a-426c-bb39-be4065e93e4f/lulesh-1ca67244-0492-454c-b052-3db81d85fc83/lulesh-1ca67244-0492-454c-b052-3db81d85fc83.err
#SBATCH -n 8
module load charliecloud

srun mkdir -p /tmp
srun ch-tar2dir /home/bee/container_archive/jtronge%lulesh:mpi-no-openmp.tar.gz /tmp
srun ch-run /tmp/jtronge%lulesh:mpi-no-openmp --cd /home/bee -- /lulesh2.0 -s 60 -i 600
srun rm -rf /tmp/jtronge%lulesh:mpi-no-openmp
