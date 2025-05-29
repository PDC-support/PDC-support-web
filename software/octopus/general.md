Octopus is a scientific program aimed at the ab initio virtual experimentation on a hopefully ever-increasing range of system types. Electrons are described quantum-mechanically within density-functional theory (DFT), in its time-dependent form (TDDFT) when doing simulations in time. Nuclei are described classically as point particles. Electron-nucleus interaction is described within the pseudopotential approximation.
https://octopus-code.org/

## How to use

To use this module do
ml PDC/<version>
ml octopus/15.1-cpeGNU-24.11
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
ml octopus/15.1-cpeGNU-24.11

srun octopus inp > out.log
```


Assuming the script is named jobscriptoctopus.sh, it can be submitted using:
```
sbatch jobscriptoctopus.sh
```

Please consult the official Octopus documentation for more details

