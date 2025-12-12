ABINIT is a package whose main program allows one to find the total energy, charge density and electronic structure of systems made of electrons and nuclei (molecules and periodic solids) within Density Functional Theory (DFT), using pseudopotentials and a planewave or wavelet basis.
For more information, please visit [https://www.abinit.org](https://www.abinit.org)

## How to use

To use this module do

```
ml PDC/<version>
ml abinit/10.2.7-cpeGNU-24.11
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
ml abinit/10.2.7-cpeGNU-24.11

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

srun -n 8 abinit <input file>.abi > out.log

echo "Script finished at `date` on `hostname`"
```

Assuming the script is named jobscriptABINIT.sh, it can be submitted using
```
sbatch jobscriptABINIT.sh
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
