Octopus is a scientific program aimed at the ab initio virtual experimentation on a hopefully ever-increasing range of system types. Electrons are described quantum-mechanically within density-functional theory (DFT), in its time-dependent form (TDDFT) when doing simulations in time. Nuclei are described classically as point particles. Electron-nucleus interaction is described within the pseudopotential approximation.
https://octopus-code.org/

## How to use

To use this module do
ml PDC/<version>
ml octopus/16.3-cpeGNU-24.11
Below follows an example job script for Octopus.
```
#!/bin/bash

# time allocation
#SBATCH -A <your-project-account>

# name of this job
#SBATCH -J octopus-job

# partition
#SBATCH -p main

# wall time for this job
#SBATCH -t 01:00:00

# number of nodes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1

ml PDC/<version>
ml octopus/16.3-cpeGNU-24.11

srun octopus inp > out.log
```


Assuming the script is named jobscriptoctopus.sh, it can be submitted using:
```
sbatch jobscriptoctopus.sh
```

## GPU Support

Below follows an example job script for Octopus, for running on one Dardel GPU node
using 8 MPI tasks per node (corresponding to one MPI task per GPU) and 8 OpenMP threads.
You need to replace *pdc.staff* with an active project that you belong to.
**Note: This script is a simple template. For efficient calculation the script needs to
be augmented with settings to pin appropriately the computation threads to the CCDs
and GCD.**

```
#!/bin/bash
#SBATCH -A pdc.staff
#SBATCH -p gpu
#SBATCH -J octopus
#SBATCH -t 02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=8

# Number and placement of OpenMP threads
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=8
export OMP_PLACES=cores
export OMP_PROC_BIND=false
export MPICH_GPU_SUPPORT_ENABLED=1

ml PDC/24.11
ml octopus/16.3-cpeGNU-24.11-gpu

echo "Script initiated at `date` on `hostname`"

srun --hint=nomultithread octopus inp > out.log

echo "Script finished at `date` on `hostname`"
```


Assuming the script is named jobscriptoctopus.sh, it can be submitted using
```
sbatch jobscriptoctopus.sh
```

Octopus is also available as builds for the NVIDIA Grace Hopper nodes. Here is an example job script for running on one node, with one task per GPU.

```bash
#!/bin/bash
#SBATCH -A pdc.staff
#SBATCH -J octopus
#SBATCH -t 02:00:00
#SBATCH -p gpugh
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -c 72
#SBATCH --gpus-per-task 1

# Run time modules and executable paths
ml PDC/25.03
ml octopus/16.3

# Runtime environment
export MPICH_GPU_SUPPORT_ENABLED=1
export PMPI_GPU_AWARE=1
export OMP_NUM_THREADS=72
export OMP_PLACES=cores
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

echo "Script initiated at `date` on `hostname`"
srun --hint=nomultithread octopus > out.log
echo "Script finished at `date` on `hostname`"
```

Please consult the official Octopus documentation for more details

## How to build Octopus

The program was installed using [EasyBuild](https://docs.easybuild.io/en/latest/).
A build in your local file space can be done with

```bash
ml PDC/24.11
ml easybuild-user/4.9.4
eb octopus-16.3-cpeGNU-24.11.eb --robot
```

A build for NVIDIA Grace Hopper nodes can be done with

```bash
# Build instructions for Octopus on Dardel Grace Hopper nodes

# Download the Octopus source code
wget https://octopus-code.org/download/16.3/octopus-16.3.tar.xz
tar xf octopus-16.3.tar.xz
cd octopus-16.3

# Load dependencies
ml PDC/25.03
ml PrgEnv-gnu
ml gcc-native/13.2
ml cudatoolkit/24.11_12.6
ml craype-accel-nvidia90
ml cray-libsci/25.03.0
ml cray-fftw/3.3.10.10
ml cmake/4.1.2
ml ninja/1.12.1
ml gsl/2.8
ml libxc/7.0.0

export CXX=CC
export CC=cc
export FC=ftn

# Configure
cmake -B ./buildGH1 \
    -GNinja \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX=/pdc/software/25.03/other/octopus/16.3 \
    -D OCTOPUS_MPI=ON \
    -D OCTOPUS_OpenMP=ON \
    -D OCTOPUS_FFTW=ON \
    -D OCTOPUS_CUDA=ON \
    -D CMAKE_POLICY_VERSION_MINIMUM=3.5 \
    > ./buildGH1/BuildOctopus_cmake.txt 2>&1

# Compile and install
cmake --build ./buildGH1 > ./buildGH1/BuildOctopus_make.txt 2>&1
MPIEXEC=srun ctest --test-dir ./buildGH1 -L short-run > ./buildGH1/BuildOctopus_test.txt 2>&1
cmake --install ./buildGH1 > ./buildGH1/BuildOctopus_install.txt 2>&1
```
