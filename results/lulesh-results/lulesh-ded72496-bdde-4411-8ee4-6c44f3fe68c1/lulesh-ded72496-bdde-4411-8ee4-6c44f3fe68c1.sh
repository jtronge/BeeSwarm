#! /bin/bash
#SBATCH --job-name=lulesh-ded72496-bdde-4411-8ee4-6c44f3fe68c1
#SBATCH --output=/home/bee/.beeflow/workflows/6735b413-27eb-4801-8c2e-f0ff6fc7c480/lulesh-ded72496-bdde-4411-8ee4-6c44f3fe68c1/lulesh-ded72496-bdde-4411-8ee4-6c44f3fe68c1.out
#SBATCH --error=/home/bee/.beeflow/workflows/6735b413-27eb-4801-8c2e-f0ff6fc7c480/lulesh-ded72496-bdde-4411-8ee4-6c44f3fe68c1/lulesh-ded72496-bdde-4411-8ee4-6c44f3fe68c1.err
#SBATCH -n 27
module load charliecloud

srun mkdir -p /tmp
srun ch-tar2dir /home/bee/container_archive/jtronge%lulesh:mpi-no-openmp.tar.gz /tmp
srun ch-run /tmp/jtronge%lulesh:mpi-no-openmp --cd /home/bee -- /lulesh2.0 -s 60 -i 600
srun rm -rf /tmp/jtronge%lulesh:mpi-no-openmp
