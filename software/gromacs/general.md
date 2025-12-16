GROMACS is a versatile package to perform molecular dynamics, i.e. simulate the Newtonian equations of motion for systems with hundreds to millions of particles. It provides extremely high performance through custom algorithmic optimizations. More information on the [GROMACS homepage](https://www.gromacs.org).
Several versions of GROMACS are installed at PDC. Generally, it is recommended to use the most recent version since it can be expected to be faster,
more stable and less memory demanding.
Information on how to run GROMACS on AMD GPU nodes of an HPE Cray EX cluster can be found in [How to run GROMACS efficiently on the LUMI supercomputer](https://zenodo.org/records/10683366).

## How to use

GROMACS is highly tuned for quite efficient use of HPC resources.
Special assembly kernels make its core compute engine one of the fastest MD
simulation programs.

## How to user
You can check for available GROMACS modules with
```
ml spider gromacs
```

For example, to load the module for GROMACS 2024.2/
```
ml PDC/<version>
ml gromacs/2025.1-cpeGNU-24.11
```
To see what environment variables are set when loading the module
```
ml gromacs/2025.1-cpeGNU-24.11
```
Preprocessing input files (molecular topology, initial coordinates and
mdrun parameters) to create a portable run input (.tpr) file can be run
in a batch job by
```
srun -n 1 gmx_mpi grompp -c conf.gro -p topol.top -f grompp.mdp
```
Gromacs also contains a large number of other pre- and post-processing tools.
A list of available commands can be seen by
```
srun -n 1 gmx_mpi help commands
```
The GROMACS module provide up to four main versions of the GROMACS suite
##
- *gmx* : The MD engine binary without MPI, but with openMP threading. Useful if GROMACS is executed for preprocessing or running analysis tools on a compute node.
- *gmx_mpi* : The MD engine binary with MPI support. This is the one that researchers would use most of the time.
- *gmx_d* : Same as *gmx* above but in double precision.
- *gmx_mpi_d* : Same as *gmx_mpi* above but in double precision.

All tools from the GROMACS suite can be launched using any of the above
versions. Please note that they should be launched on the compute node(s).
Remember to *always* use in your scripts *srun* in front of the actual GROMACS
command! Here is an example script that requests 2 nodes:

```
#!/bin/bash
#SBATCH -J my_gmx_job
#SBATCH -A naissYYYY-X-XX
#SBATCH -p main
#SBATCH -t 01:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128

ml PDC/<version>
ml gromacs/2025.1-cpeGNU-24.11

export OMP_NUM_THREADS=1

srun -n 1 gmx_mpi grompp -c conf.gro -p topol.top -f grompp.mdp
srun gmx_mpi mdrun -s topol.tpr -deffnm gmx_md
```

The executables for Dardel GROMACS GPU nodes have been built with the AdaptiveCPP backend for AMD GPUs

To load the GROMACS module for AMD GPUs

```
ml PDC/24.11
ml cp2k/2025.2-cpeGNU-24.11-gpu
```

Below follows an example job script for GROMACS, for running on one Dardel GPU node
using 8 MPI tasks per node (corresponding to one MPI task per GPU) and 8 OpenMP threads.
You need to replace *pdc.staff* with an active project that you belong to.
**Note: This script is a simple template. For efficient calculation the script needs to
be augmented with settings to pin appropriately the computation threads to the CCDs
and GCD.**

```bash
#!/bin/bash
#SBATCH -J my_gmx_job
#SBATCH -A pdc.staff
#SBATCH -p gpu
#SBATCH -t 24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gpus-per-node=8

ml PDC/24.11
ml gromacs/2025.2-gpu

export OMP_NUM_THREADS=1
export MPICH_GPU_SUPPORT_ENABLED=1

echo "Script initiated at `date` on `hostname`"
srun gmx_mpi mdrun -s topol.tpr -deffnm gmx_md
echo "Script finished at `date` on `hostname`"
```

## How to build GROMACS

The builds of GROMACS for AMD CPU nodes are mainly done with [EasyBuild](https://docs.easybuild.io/en/latest/)
using **cpeGNU** and **cpeCray** toolchains.
A build in your local file space can be done with

```bash
ml PDC/24.11
ml easybuild-user/4.9.4
eb gromacs-2025.1-cpeGNU-24.11.eb --robot
```

See also [Installing software using EasyBuild](https://support.pdc.kth.se/doc/software_development/easybuild/).

The builds for AMD GPU nodes are done with the **PrgEnv-amd** toolchain.

```bash
#!/bin/bash
# Build instructions for GROMACS 2025.2 on Dardel

# Load the environment
ml PDC/24.11
ml craype-accel-amd-gfx90a
ml swap PrgEnv-cray/8.6.0 PrgEnv-amd/8.6.0
ml swap amd/6.0.0 amd/6.3.3
ml cray-mpich/8.1.31
ml cray-fftw/3.3.10.9
ml cray-libsci/24.11.0
ml cmake/4.0.1
ml rocm/6.3.3
ml boost/1.79.0-nompi

# GROMACS 2025.2
# Download and untar the source code
wget https://gitlab.com/gromacs/gromacs/-/archive/v2025.2/gromacs-v2025.2.tar.gz
tar xvf gromacs-v2025.2.tar.gz
cd gromacs-v2025.2/

# Set AdaptiveCpp environment variables
export PATH=/pdc/software/24.11/other/adaptivecpp/25.02.0/bin:$PATH
export LIBRARY_PATH=/pdc/software/24.11/other/adaptivecpp/25.02.0/lib:$LIBRARY_PATH
export CPATH=/pdc/software/24.11/other/adaptivecpp/25.02.0/include:$CPATH

# Configure
mkdir build
cd build
cmake ../ \
-DCMAKE_C_COMPILER=amdclang \
-DCMAKE_CXX_COMPILER=amdclang++ \
-Dadaptivecpp_DIR=/pdc/software/24.11/other/adaptivecpp/25.02.0/lib/cmake/AdaptiveCpp \
-DCMAKE_BUILD_TYPE=Release \
-DGMX_BUILD_OWN_FFTW=OFF \
-DGMX_SIMD=AVX2_256 \
-DGMX_OPENMP=ON \
-DGMXAPI=OFF \
-DGMX_GPU=SYCL \
-DGMX_SYCL=ACPP \
-DACPP_TARGETS='hip:gfx90a' \
-DGMX_GPU_FFT_LIBRARY=vkfft \
-DGMX_CYCLE_SUBCOUNTERS=ON \
-DGMX_MPI=ON \
-DMPI_CXX_SKIP_MPICXX=ON \
-DMPI_CXX_COMPILER=CC -DGMX_BLAS_USER=${CRAY_LIBSCI_PREFIX_DIR}/lib/libsci_amd.so \
-DGMX_LAPACK_USER=${CRAY_LIBSCI_PREFIX_DIR}/lib/libsci_amd.so \
-DCMAKE_{EXE,SHARED}_LINKER_FLAGS=-fuse-ld=ld \
-DCMAKE_INSTALL_PREFIX=/pdc/software/24.11/other/gromacs/2025.2-gpu > BuildGROMACS_CMakeLog.txt 2>&1

# Build and install
make -j 64 > BuildGROMACS_make.txt 2>&1
make install

# Set runtime environment
export LD_LIBRARY_PATH=/pdc/software/24.11/other/adaptivecpp/25.02.0/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/pdc/software/24.11/other/gromacs/2025.2-gpu/lib:$LD_LIBRARY_PATH
export PATH=/pdc/software/24.11/other/gromacs/2025.2-gpu/bin:$PATH
```
