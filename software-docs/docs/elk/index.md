---
title: Information about elk
keywords:
  - Applications
  - Physics
---
# Elk

## Installed versions

| Resource | Version |
|---|---|
| Dardel/cpe23.12 | 10.0.15, 9.5.14 |
| Dardel/cpe23.03 | 9.2.12 |

## General information

Elk is an all-electron full-potential linearised augmented-planewave (FP-LAPW) code [https://elk.sourceforge.net](https://elk.sourceforge.net). Designed to be as developer friendly as possible so that new developments in the field of density functional theory (DFT) can be added quickly and reliably.

## How to use

The Elk installation contained in this module was built with support for the programs and libraries Libxc and Wannier90.
To display info on which environment variables are set when loading the module, use
```
ml PDC/<version>
ml show elk/10.0.15-cpeGNU-23.12
```
To load the Elk module
```
ml PDC/<version>
ml elk/10.0.15-cpeGNU-23.12
```
The species files are found in ``EBROOTELK/species``
Examples are provided in ``$EBROOTELK/examples``

# Running on the Batch system
Sample job script to queue an Elk job with 16 MPI ranks, and 8 openMP threads

```
#!/bin/bash

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A <project name>

# The name of the script is myjob
#SBATCH -J myjob

# partition
#SBATCH -p main

# 10 hours wall-clock time will be given to this job
#SBATCH -t 10:00:00

# Number of nodes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=16

ml PDC/23.12
ml elk/10.0.15-cpeGNU-23.12

export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=8
export OMP_PLACES=cores
export OMP_PROC_BIND=false
export OMP_STACKSIZE=256M
ulimit -Ss unlimited

echo "Script initiated at `date` on `hostname`"

srun -n 16 elk > out.log

echo "Script finished at `date` on `hostname`"
```

For information on how to submit jobs on Dardel, see [Queueing jobs](https://support.pdc.kth.se/doc/contact/contact_support/-docs/run_jobs/job_scheduling/).

## How to build Elk

The program was installed using EasyBuild https://docs.easybuild.io/en/latest/.
A build in your local file space can be done with

```bash
ml PDC/23.12
ml easybuild-user/4.9.1
eb elk-10.0.15-cpeGNU-23.12.eb --robot
```

See also [Installing software using EasyBuild](https://support.pdc.kth.se/doc/contact/contact_support/-docs/software_development/easybuild/).

## Species files, example input files, and Elk make.inc file.

Elk species files and example input files can be found
in the directories
```bash
$EBROOTELK/species
$EBROOTELK/examples
```
For the case that you would like to build a custom version
of Elk, you can find the Elk `make.inc` file which was generated
when building with EasyBuild at
```bash
$EBROOTELK/make.inc
```

