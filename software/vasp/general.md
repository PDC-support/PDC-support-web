The Vienna Ab initio Simulation Package (VASP) is a computer program for atomic
scale materials modelling, e.g. electronic structure calculations and
quantum-mechanical molecular dynamics, from first principles.
For more information see the VASP home page [https://vasp.at](https://vasp.at)
and the [VASP wiki](https://www.vasp.at/wiki).

# Licenses
VASP is not free software and requires a software license.
If you want to use VASP please contact us with information
of the e-mail address that you have listed in the VASP global portal.

## How to use VASP

## General observations
- VASP is not helped by hyper-threading
- Running on fewer than 128 tasks per node allocates more memory to each MPI task. This can in some cases improve performance and is necessary if your job crashes with an out-of-memory (OOM) error. Further information can be found on the VASP wiki pages [Memory_requirements](https://www.vasp.at/wiki/index.php/Memory_requirements) and [Not_enough_memory](https://www.vasp.at/wiki/index.php/Not_enough_memory).

## Parallelization settings
Parallelization over k-points is recommended when it is possible to do so. In practice,
KPAR should be set to be equal to the number of nodes. Please also make sure that the
k-points can be evenly distributed over nodes. For example, a calculation with 15 k-points
can run on 15 nodes with KPAR=15. NCORE determines the number of cores that work on an
individual orbital. A recommended value for NCORE is 16.

## How to choose the number of cores
### Rule of thumb
- 1 atom per core = Good
- 0.5 atom per core = Could work (but bad efficiency and time wasted)
- <0.5 atom per core = Don't do it
### Explanation of above
- The number of bands is more important than the number of atoms, but typically
you have about 4 bands/atom in VASP.

### Checklist:
- Check how many you have in the calculation. Let's call this "NB".
- Cores = NB is best you can do.
- For better efficiency, typically 90%+, aim for at least 4 bands per core, i.e. Cores = NB/4
- If you can use k-point parallelization ("KPAR"), use it! It improves scaling a lot. You can run up to cores = #kpts * NB / 4.
- You have now determined the number of cores.
- Look at this number. Does it look "strange"? Try to adjust the number of
bands to make the number of cores more even, .e.g we don't want a prime number.
Good numbers are multiple of 4,8,12,16 etc. For example, 512 bands is better
than 501 (=3x167).
- Calculate the number of nodes necessary, e.g. 512 cores (128 cores/node) = 4 compute nodes.
- For a wide calculation with less than 4 bands per core, try decreasing the
  number of cores per node to 64, or even 32. You may also have to do this get
  memory available for each MPI rank.

## Vasp Filenames
- **vasp** : this is normal regular VASP version for calculations using >1 k-point.
- **vasp-gamma** : gamma-point only version of VASP. Use this one if you only have the gamma point. It is much faster and uses less memory.
- **vasp-noncollinear** : VASP for noncollinear and spin-orbit coupling calculations.

## BEEF functionals
This version of VASP has been compiled with support for [BEEF functionals](https://confluence.slac.stanford.edu/display/SUNCAT/BEEF+Functional+Software).

## VASP VTST Tools
The [VTST](http://theory.cm.utexas.edu/vtsttools) extension to VASP enables finding saddle points and evaluating
transition state theory (TST) rate constants with VASP.

## VTST Scripts
The [VTST Perl scripts](https://theory.cm.utexas.edu/vtsttools/scripts.html) are available to perform common tasks to
help with VASP calculations, and particularly with transition state finding.

## VASPsol
[VASPsol](https://github.com/henniggroup/VASPsol) is an implementation of an implicit solvation model that describes the effect of electrostatics, cavitation, and dispersion on the interaction between a solute and solvent.
Full documentation on how to use [VASPsol documentation](https://github.com/henniggroup/VASPsol/blob/master/docs/USAGE.md).
### Short how to do
- Do a vacuum calculation for your system first and save the wavefunction file WAVECAR by specifying LWAVE = .TRUE. in the INCAR file.
- Start the solvation calculation from the vacuum WAVECAR, specify ISTART = 1 in the INCAR file.
- The solvation parameters are read from the INCAR file.
- In the simplest case the only parameter that need to be set is the solvation flag LSOL = .TRUE.

## Potential files and vdW kernel
Projector augmented wave (PAW) potentials can be found at ``/pdc/software/24.11/other/vasp/potpaw-64/``

To use one of the nonlocal vdW functionals one needs to put the file vdw_kernel.bindat into the run directory (along with INCAR, POSCAR, POTCAR and KPOINTS). This file can be found at ``/pdc/software/24.11/other/vasp/vdw_kernel/vdw_kernel.bindat``.

## Running Vasp
Here is an example of a job script requesting 128 MPI processes per node:
```
#!/bin/bash

#SBATCH -A naissYYYY-X-XX
#SBATCH -J my_vasp_job
#SBATCH -t 01:00:00
#SBATCH -p main

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128

module load PDC/24.11
module load vasp/6.4.3-vanilla

export OMP_NUM_THREADS=1

srun --hint=nomultithread vasp
```
Since OpenMP is supported by this module, you can also submit a job
requesting 64 MPI processes per node and 2 OpenMP threads per MPI
process, using the job script below. Please note that in this case
you need to specify ``--cpus-per-task``, ``OMP_NUM_THREADS``, and ``OMP_PLACES``.

Please also note that it is necessary set the ``SRUN_CPUS_PER_TASK``
environment variable in the job script so that ``srun`` can work as expected,
see [SLURM documentation](https://slurm.schedmd.com/srun.html).
```
#!/bin/bash

#SBATCH -A naissYYYY-X-XX
#SBATCH -J my_vasp_job
#SBATCH -t 01:00:00
#SBATCH -p main

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=2

module load PDC/24.11
module load vasp/6.4.3-vanilla

export OMP_NUM_THREADS=2
export OMP_PLACES=cores

export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

srun --hint=nomultithread vasp
```
