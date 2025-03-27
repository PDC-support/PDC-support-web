---
title: Information about uppasd
keywords:
  - Applications
  - Physics
---
# Uppasd

## Installed versions

| Resource | Version |
|---|---|
| Dardel/cpe23.12 | 6.0.2 |
| Dardel/cpe23.03 | 6.0.2 |

## General information

The Uppsala Atomistic Spin Dynamics (UppASD) software package is a simulation suite to study magnetization dynamics by means of the atomistic version of the Landau-Lifshitz-Gilbert (LLG) equation. For more information see [https://github.com/UppASD/UppASD](https://github.com/UppASD/UppASD).

## How to use

The UppASD files can be accessed by loading the appropriate modules. To see which versions of UppASD are available use the command
```bash
ml avail uppasd
ml spider uppasd
```
To load the 6.0.2 version of the program
```bash
ml PDC/<version>
ml uppasd/6.0.2-cpeGNU-23.12
```
The binary is ``sd``
Examples are provided in ``$EBROOTUPPASD/examples``
The code is documented in the [UppASD manual](https://uppasd.github.io/UppASD-manual) and in technical notes in the directory ``$UPPASD_DOCS``.
A tutorial with examples and exercises on atomistic spin-dynamics are contained in the [UppASD tutorial](https://uppasd.github.io/UppASD-tutorial).

## Running on the batch system
Sample job script to queue an UppASD job with 16 openMP threads on cores on the shared partition of Dardel

```bash
#!/bin/bash
#SBATCH -A <project name>     # Set the allocation to be charged for this job
#SBATCH -J myjob              # The name of the script is myjob
#SBATCH -t 02:00:00           # 2 hours wall-clock time
#SBATCH -p shared             # The partition
#SBATCH -c 16                 # Number of cpus per task

ml PDC/<version>
ml uppasd/6.0.2-cpeGNU-23.12

export OMP_NUM_THREADS=16

echo "Script initiated at `date` on `hostname`"

sd > out.log

echo "Script finished at `date` on `hostname`"
```

For information on how to submit jobs on Dardel, see [Queueing jobs](https://www.pdc.kth.se/support/documents/run_jobs/queueing_jobs.html).

## User Graphic Interface
A `Python` based `QT` GUI for the code is available at ``$EBROOTUPPASD/ASD_GUI``.
### Features
- Visualization of outputs via `VTK`.
- Plotting of several quantities via integrated `Matplotlib` functionalities.
- Automatic generation of input files for `UppASD`.

The output from UppASD simulations are supported by the [SpinView](https://mxjk851.github.io/SpinView/) interactive visual analysis tool for multi-scale computational magnetism.

## Tools for preprocessing and postprocessing
A collection of scripts for preprocessing and postprocessing of UppASD input and output files can be found in ``$EBROOTUPPASD/ASD_Tools``.

## How to build UppASD

The program was installed using EasyBuild https://docs.easybuild.io/en/latest/.
A build in your local file space can be done with

```bash
ml PDC/23.12
ml easybuild-user/4.9.1
eb uppasd-6.0.2-cpeGNU-23.12.eb --robot
```

See also [Installing software using EasyBuild](https://support.pdc.kth.se/doc/support-docs/software_development/easybuild/).

