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
ml quantum-espresso/7.4.1-cpeGNU-24.11
```
Here is an example of a job script requesting 128 MPI processes per node:
```
#!/bin/bash

#SBATCH -J myjob
#SBATCH -A snicYYYY-X-XX
#SBATCH -p main
#SBATCH -t 01:00:00

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128

ml PDC/<version>
ml quantum-espresso/7.4.1-cpeGNU-24.11

export OMP_NUM_THREADS=1

srun pw.x -in myjob.in > myjob.out
```
Since OpenMP is supported by this module, you can also submit a job
requesting 64 MPI processes per node and 2 OpenMP threads per MPI
process, using the job script below. Please note that in this case
you need to specify ``--cpus-per-task``, ``OMP_NUM_THREADS``, and ``OMP_PLACES``,
and that the value of ``--cpus-per-task`` is equal to 2x ``OMP_NUM_THREADS``,
because AMD's simultaneous multithreading (SMT) is enabled.
```
#!/bin/bash

#SBATCH -J myjob
#SBATCH -A snicYYYY-X-XX
#SBATCH -p main
#SBATCH -t 01:00:00

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=4

ml PDC/<version>
ml quantum-espresso/7.4.1-cpeGNU-24.11

export OMP_NUM_THREADS=2
export OMP_PLACES=cores

srun pw.x -in myjob.in > myjob.out
```