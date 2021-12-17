#! /bin/bash
#SBATCH --job-name=lulesh-c922f730-3b72-4777-85a0-94a02e9d6085
#SBATCH --output=/home/bee/.beeflow/workflows/65619d8e-03d3-4de6-aa3f-8bded9c0ca7c/lulesh-c922f730-3b72-4777-85a0-94a02e9d6085/lulesh-c922f730-3b72-4777-85a0-94a02e9d6085.out
#SBATCH --error=/home/bee/.beeflow/workflows/65619d8e-03d3-4de6-aa3f-8bded9c0ca7c/lulesh-c922f730-3b72-4777-85a0-94a02e9d6085/lulesh-c922f730-3b72-4777-85a0-94a02e9d6085.err
#SBATCH -n 125
module load charliecloud

srun mkdir -p /tmp
srun ch-tar2dir /home/bee/container_archive/jtronge%lulesh:mpi-no-openmp.tar.gz /tmp
srun ch-run /tmp/jtronge%lulesh:mpi-no-openmp --cd /home/bee -- /lulesh2.0 -s 60 -i 600
srun rm -rf /tmp/jtronge%lulesh:mpi-no-openmp
