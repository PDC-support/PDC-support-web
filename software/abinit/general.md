ABINIT is a package whose main program allows one to find the total energy, charge density and electronic structure of systems made of electrons and nuclei (molecules and periodic solids) within Density Functional Theory (DFT), using pseudopotentials and a planewave or wavelet basis.
For more information, please visit [https://www.abinit.org](https://www.abinit.org)

## How to use

To use this module do

```
ml PDC/<version>
ml abinit/10.4.7-cpeGNU-24.11
```

Below follows an example job script for ABINIT.
```
#!/bin/bash

# time allocation
#SBATCH -A <your-project-account>

# name of this job
#SBATCH -J abinit-job

# partition
#SBATCH --partition=main

# wall time for this job
#SBATCH -t 01:00:00

# number of nodes
#SBATCH --nodes=1

# number of MPI processes per node
#SBATCH --ntasks-per-node=128

ml PDC/24.11
ml abinit/10.4.7-cpeGNU-24.11

echo "Script initiated at `date` on `hostname`"

export ABI_PSPDIR=<pseudo potentials directory>

srun -n 128 abinit <input file>.abi > out.log

echo "Script finished at `date` on `hostname`"
```

Assuming the script is named ``jobscriptabinit.sh``, it can be submitted using:
```
sbatch jobscriptabinit.sh
```

## GPU Support

**Support for GPUs in ABINIT is experimental, see https://docs.abinit.org/INSTALL_gpu/.**

Below follows an example job script for ABINIT, for running on one Dardel GPU node
using 8 MPI tasks per node (corresponding to one MPI task per GPU) and 8 OpenMP threads.
You need to replace *pdc.staff* with an active project that you belong to.
**Note: This script is a simple template. For efficient calculation the script needs to
be augmented with settings to pin appropriately the computation threads to the CCDs
and GCD.**

```
#!/bin/bash
#SBATCH -A pdc.staff
#SBATCH -p gpu
#SBATCH -J abinit
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
ml abinit/10.4.7-cpeGNU-24.11-gpu

echo "Script initiated at `date` on `hostname`"

export ABI_PSPDIR=<pseudo potentials directory>

srun --hint=nomultithread abinit <input file>.abi > out.log

echo "Script finished at `date` on `hostname`"
```

Assuming the script is named jobscriptABINIT.sh, it can be submitted using
```
sbatch jobscriptABINIT.sh
```

Quantum Espresso is also available as builds for the NVIDIA Grace Hopper nodes. Here is an example job script for running on two nodes, with one task per GPU.

```bash
#!/bin/bash
#SBATCH -A pdc.staff
#SBATCH -J abinit
#SBATCH -t 02:00:00
#SBATCH -p gpugh
#SBATCH -N 2
#SBATCH -n 8
#SBATCH -c 72
#SBATCH --gpus-per-task 1

# Run time modules and executable paths
ml PDC/25.03
ml abinit/10.4.7

# Runtime environment
export MPICH_GPU_SUPPORT_ENABLED=1
export PMPI_GPU_AWARE=1
export OMP_NUM_THREADS=72
export OMP_PLACES=cores
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

echo "Script initiated at `date` on `hostname`"
srun --hint=nomultithread abinit <input file>.abi > out.log
echo "Script finished at `date` on `hostname`"
```

Please consult the official ABINIT documentation for more details
[https://www.abinit.org](https://www.abinit.org).

## How to build ABINIT

The program was installed using [EasyBuild](https://docs.easybuild.io/en/latest/).
A build in your local file space can be done with

```bash
ml PDC/24.11
ml easybuild-user/4.9.4
eb abinit-10.4.7-cpeGNU-24.11-gpu.eb --robot
```

A build for NVIDIA Grace Hopper nodes can be done with

```bash
# Build instructions for ABINIT on Dardel Grace Hopper nodes

# Download and untar the source code
wget wget https://forge.abinit.org/abinit-10.4.7.tar.gz
tar xf abinit-10.4.7.tar.gz
cd abinit-10.4.7

# Load the environment, GNU and CUDA toolchain
ml PrgEnv-gnu
ml gcc-native/13.2
ml cudatoolkit/24.11_12.6
ml cray-fftw/3.3.10.10
ml cray-hdf5-parallel/1.14.3.5
ml cray-netcdf-hdf5parallel/4.9.0.17
ml craype-accel-nvidia90
ml cmake/4.1.2
ml PDC/25.03
ml libxc/7.0.0
ml wannier90/3.1.0

export FC=ftn
export CC=cc
export CXX=CC
export GPU_ARCH=90
export WANNIER90_LIBS="-L/pdc/software/25.03/other/wannier90/3.1.0/lib -lwannier"

./configure \
    --with-mpi="yes" \
    --enable-openmp="yes" \
    --enable-mpi-gpu-aware \
    --with-fft-flavor=fftw3 FFTW3_LIBS="-L${FFTW_ROOT} -lfftw3f -lfftw3" \
    --with-netcdf="${CRAY_NETCDF_HDF5PARALLEL_DIR}" \
    --with-netcdf-fortran="${CRAY_NETCDF_HDF5PARALLEL_DIR}" \
    --with-hdf5="${CRAY_HDF5_PARALLEL_DIR}" \
    --with-cuda=/opt/nvidia/hpc_sdk/Linux_aarch64/24.11/cuda/12.6 \
    --with-libxc=/pdc/software/25.03/other/libxc/7.0.0/ \
    --with-wannier90=/pdc/software/25.03/other/wannier90/3.1.0/ \
    --prefix=/pdc/software/25.03/other/abinit/10.4.7

# Build and install
make -j 72
make install
```