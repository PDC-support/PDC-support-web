Quantum ESPRESSO is an integrated suite of open-Source computer codes for
electronic-structure calculations and materials modeling at the nanoscale. It
is based on density-functional theory, plane waves, and pseudopotentials.  For
more information see [https://www.quantum-espresso.org](https://www.quantum-espresso.org).

## How to use

# General considerations
- You should **always** use the option ``disk_io=low``. With this option the wave functions are only written at the end of the job rather than after every intermediate step. This will substantially reduce the load on the disk systems and make your job run faster.
- Also it is **NOT allowed** to run the phonon part of Quantum ESPRESSO (i.e.  ``ph.x``) on Dardel. This is because the phonon part does not seem to have the equivalent of ``disk_io=low`` and therefore creates more IO than the shared Lustre file system can handle.

## Running Quantum ESPRESSO
To use this module do
```
ml PDC/<version>
ml quantum-espresso/7.5.0-cpeGNU-24.11
```
Here is an example of a job script requesting 128 MPI processes on one node:
```
#!/bin/bash

#SBATCH -J qejob
#SBATCH -A naissYYYY-X-XX
#SBATCH -p main
#SBATCH -t 01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128

ml PDC/<version>
ml quantum-espresso/7.5.0-cpeGNU-24.11

export OMP_NUM_THREADS=1

srun pw.x -in myjob.in > myjob.out
```
Since OpenMP is supported by this module, you can also submit a job
requesting 64 MPI processes per node and 2 OpenMP threads per MPI
process, using the job script below. Please note that in this case
you need to specify ``--cpus-per-task``, ``OMP_NUM_THREADS``, and ``OMP_PLACES``.
```bash
#!/bin/bash

#SBATCH -J qejob
#SBATCH -A naissYYYY-X-XX
#SBATCH -p main
#SBATCH -t 01:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=2

ml PDC/<version>
ml quantum-espresso/7.5.0-cpeGNU-24.11

export OMP_NUM_THREADS=2
export OMP_PLACES=cores
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

srun --hint=nomultithread pw.x -in myjob.in > myjob.out
```

Quantum Espresso is also available as builds for the NVIDIA Grace Hopper nodes. Here is an example job script for running on two nodes, with one task per GPU.

```bash
#!/bin/bash
#SBATCH -A pdc.staff
#SBATCH -J qe
#SBATCH -t 02:00:00
#SBATCH -p gpugh
#SBATCH -N 2
#SBATCH -n 8
#SBATCH -c 72
#SBATCH --gpus-per-task 1

# Run time modules and executable paths
ml PDC/25.03
ml quantum-espresso/7.5.0

# Runtime environment
export MPICH_GPU_SUPPORT_ENABLED=1
export PMPI_GPU_AWARE=1
export OMP_NUM_THREADS=72
export OMP_PLACES=cores
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

echo "Script initiated at `date` on `hostname`"
srun --hint=nomultithread pw.x -in myjob.in > myjob.out
echo "Script finished at `date` on `hostname`"
```

## How to build Quantum Espresso

The builds for AMD CPU nodes were installed using [EasyBuild](https://docs.easybuild.io/en/latest/).
A build in your local file space can be done with

```bash
ml PDC/24.11
ml easybuild-user/4.9.4
eb quantum-espresso-7.5.0-cpeGNU-24.11.eb --robot
```

See also [Installing software using EasyBuild](https://support.pdc.kth.se/doc/support-docs/software_development/easybuild/).

A build for NVIDIA Grace Hopper nodes can be done with

```bash
# Build instructions for Quantum Espresso on Dardel Grace Hopper nodes

# Download and untar the source code
wget https://gitlab.com/QEF/q-e/-/archive/qe-7.5/q-e-qe-7.5.tar.gz
tar xvf q-e-qe-7.5.tar.gz
cd q-e-qe-7.5

# Load the environment, Gnu toolchain
ml PrgEnv-nvidia
ml cudatoolkit/24.11_12.6
ml craype-accel-nvidia90
ml cray-fftw/3.3.10.10
ml cray-hdf5/1.14.3.5
ml cmake/4.1.2

# Configure
mkdir buildNvidiaCuda
cd buildNvidiaCuda

cmake .. -DQE_ENABLE_LIBXC=0 -DQE_ENABLE_OPENMP=1 -DQE_ENABLE_SCALAPACK=1 \
      -DQE_ENABLE_WANNIER90=0 -DQE_ENABLE_ELPA=0 -DQE_ENABLE_HDF5=1 \
      -DBLAS_LIBRARIES="-L${CRAY_LIBSCI_PREFIX_DIR}/lib -lsci_nvidia_mp" \
      -DLAPACK_LIBRARIES="-L${CRAY_LIBSCI_PREFIX_DIR}/lib -lsci_nvidia_mp" \
      -DSCALAPACK_LIBRARIES="-L${CRAY_LIBSCI_PREFIX_DIR}/lib -lsci_nvidia_mp" \
      -DFFTW3_INCLUDE_DIRS="${FFTW_INC}" \
      -DQE_ENABLE_CUDA=1 \
      -DQE_ENABLE_MPI_GPU_AWARE=1 \
      -DQE_ENABLE_OPENACC=1 \
      -DCMAKE_INSTALL_PREFIX=/pdc/software/25.03/other/quantum-espresso/7.5.0 \
      > BuildQuantumEspresso_CMakeLog.txt 2>&1

# Build and install
make -j 72 all > BuildQuantumEspresso_make.txt 2>&1
make install
```
