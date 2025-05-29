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

export ABI_PSPDIR=<pseudo potentials directory>

srun -n 128 abinit <input file>.abi > out.log
```

Assuming the script is named ``jobscriptabinit.sh``, it can be submitted using:
```
sbatch jobscriptabinit.sh
```

Please consult the official ABINIT documentation for more details
[https://www.abinit.org](https://www.abinit.org).
