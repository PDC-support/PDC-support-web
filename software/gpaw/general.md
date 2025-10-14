[GPAW](https://gpaw.readthedocs.io/) is a density-functional theory (DFT) python code based on the projector-augmented wave (PAW) method and the atomic simulation environment [ASE](https://ase-lib.org/). It uses plane waves basis sets, real-space uniform grids and multigrid methods, or atom-centered basis-functions.

## How to use GPAW

## Running GPAW
Here is an example script to run GPAW on Dardel Grace Hopper GPU nodes.
Adjust the **GPAWROOT** variable as needed.

```text
#!/bin/bash
#SBATCH -A pdc.staff
#SBATCH -J gpaw
#SBATCH -t 02:00:00
#SBATCH -p gpugh
#SBATCH -n 4
#SBATCH -c 72
#SBATCH --gpus-per-task=1
#SBATCH -x nid002897

# Load modules and paths for GPAW on Dardel
ml cpeNVIDIA
export GPAWROOT=/pdc/software/25.03/other/gpaw/25.7.0
source $GPAWROOT/gpaw-25.7.0/gpawenv/bin/activate
export LD_LIBRARY_PATH=$GPAWROOT/gpaw-25.7.0/libxc-7.0.0/build/install/lib:$LD_LIBRARY_PATH

# Runtime environment
export MPICH_GPU_SUPPORT_ENABLED=1
export PMPI_GPU_AWARE=1
export OMP_NUM_THREADS=72
export OMP_PLACES=cores
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
export GPAW_NEW=1
export GPAW_USE_GPUS=1
export CUDA_VISIBLE_DEVICES=1,2,3,4

echo "Script initiated at `date` on `hostname`"
time srun -n 1 gpaw python gaasbi_gpu.py
echo "Script finished at `date` on `hostname`"
```

## How to build GPAW for NVIDIA GPUs

Load the cpeNVIDIA environment and add math_libs to LIBRARY_PATH.

```text
ml cpeNVIDIA
export LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_aarch64/24.11/math_libs/lib64:$LIBRARY_PATH
```

Download a GPAW release
```text
mkdir GPAWgpucpenvidia
cd GPAWgpucpenvidia
wget https://pypi.org/packages/source/g/gpaw/gpaw-25.7.0.tar.gz
tar xvf gpaw-25.7.0.tar.gz
cd gpaw-25.7.0
```

Load cray-python, set up a Python virtual environment
```text
ml cray-python/3.11.7
python3 -m venv gpawenv
source gpawenv/bin/activate
# Install required Python packages with pip
pip install --upgrade pip
pip install numpy scipy matplotlib ase
# Install CuPy
pip install cupy-cuda12x
```

Edit a **siteconfig_gpugh.py** file
```text
parallel_python_interpreter = True
mpi = True
compiler = 'cc'
compiler_args = []
libraries = []
library_dirs = []
include_dirs = []
extra_compile_args = [
'-g',
'-O3',
'-fopenmp',
'-fPIC',
'-Wall',
]
extra_link_args = ['-fopenmp']

libraries += ['fftw3']
library_dirs += ['/opt/cray/pe/fftw/3.3.10.8/arm_grace/lib']

#libraries += ['scalapack']
#library_dirs += ['/opt/cray/pe/libsci/24.07.0/NVIDIA/23.11/aarch64/lib']
#library_dirs += ['/opt/cray/pe/libsci_acc/24.07.0/aarch64/lib']

libraries += ['xc']
library_dirs += ['/cfs/klemming/home/h/hellsvik/Thora/Codes/GPAW/GPAWgpugh/gpaw-25.1.0/libxc-7.0.0/build/install/lib']
include_dirs += ['/cfs/klemming/home/h/hellsvik/Thora/Codes/GPAW/GPAWgpugh/gpaw-25.1.0/libxc-7.0.0/build/install/include']

define_macros += [('GPAW_ASYNC', None)]
gpu = True
gpu_target = 'cuda'
gpu_compiler = 'nvcc'
gpu_compile_args = [
'-g',
'-O3',
'-arch=compute_90',
'-code=sm_90',
#'-gencode',
#'-arch=compute_90,code=sm_90',
]
libraries += ['cudart', 'cublas']
```

and specify that this file should be used by setting
```text
export GPAW_CONFIG=siteconfig_gpugh.py
```

Build Libxc from source. First obtain the source code
```text
wget https://gitlab.com/libxc/libxc/-/archive/7.0.0/libxc-7.0.0.tar.gz
tar xvf libxc-7.0.0.tar.gz
cd libxc-7.0.0
```

Configure with CMake
```text
mkdir build
cd build
cmake .. \
-DENABLE_FORTRAN=ON \
-DCMAKE_INSTALL_LIBDIR=lib \
-DBUILD_SHARED_LIBS=ON \
-DCMAKE_INSTALL_PREFIX=`pwd`/install > BuildLibxc_CMakeLog.txt 2>&1

Build and install Libxc
```text
make -j 72 > BuildLibxc_make.txt 2>&1
cp -p XC_F03_LIB_M.mod xc_f03_lib_m.mod
cp -p XC_F03_FUNCS_M.mod xc_f03_funcs_m.mod
make install
cd ../../
export LD_LIBRARY_PATH=`pwd`/libxc-7.0.0/build/install/lib:$LD_LIBRARY_PATH
```

Build and install GPAW
```text
pip install .
```
