---
title: Information about lammps
keywords:
  - Applications
  - Molecular Dynamics
---
# Lammps

## Installed versions

| Resource | Version |
|---|---|
| Dardel/cpe23.12 | 2Aug2023, 29Aug2024 |

## General information

Lammps is a molecular dynamics simulator which can model particles at various scales and is distributed by Sandia National Laboratories.
For more information see the [LAMMPS homepage](https://www.lammps.org).

## How to use

The LAMMPS module can be loaded with
```
ml PDC/<version>
ml lammps/2Aug2023-cpeGNU-23.12
```

This will add the LAMMPS bin directory to your PATH, so that LAMMPS can be started with the command `lmp_mpi` or `lmp_omp`.
Below is an example batch script for a LAMMPS job:

```
#!/bin/bash

# time allocation
#SBATCH -A snicYYYY-X-XX
# name of this job
#SBATCH -J lammps
# wall time for this job
#SBATCH -t 01:00:00
# partition for this job
#SBATCH -p main

# number of nodes
#SBATCH --nodes=2
# number of MPI processes per node
#SBATCH --ntasks-per-node=128

ml PDC/<version>
ml lammps/2Aug2023-cpeGNU-23.12

# Run with the file infile as input and write to outfile
srun lmp < infile > outfile
```

This will run LAMMPS (`lmp`) with 256 cores (2 nodes), and will read the input specified in `infile` and write to `outfile` in the directory the job was submitted. Submit the batch script with the `sbatch` command, see also the [How to run jobs](https://www.pdc.kth.se/support/documents/run_jobs/job_scheduling.html).

## How to build LAMMPS

The program was installed using [EasyBuild](https://docs.easybuild.io/en/latest/).
A build in your local file space can be done with

```bash
ml PDC/23.12
ml easybuild-user/4.9.1
eb lammps-29Aug2024-cpeGNU-23.12.eb --robot
```

See also [Installing software using EasyBuild](https://support.pdc.kth.se/doc/support-docs/software_development/easybuild/).

## More information
For more information, refer to the [LAMMPS manual](https://docs.lammps.org/Manual.html).

