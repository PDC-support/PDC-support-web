"Amber" refers to two things: a set of molecular mechanical force fields for
the simulation of biomolecules (which are in the public domain, and are used in
a variety of simulation programs), and a package of molecular simulation
programs which includes source code and demos.
For more information see: http://ambermd.org

## How to use

Amber is the collective name for a suite of programs that allow users to
carry out molecular dynamics simulations, particularly on biomolecules.
None of the individual programs carries this name, but the various parts
work reasonably well together, and provide a powerful framework for
many common calculations.

The term Amber is also used to refer to the empirical force fields that
are implemented in Amber. It should be recognized however, that the code
and force field are separate: several other computer packages have
implemented the Amber force fields, and other force fields can be
implemented with the Amber programs.

In order to use Amber22, you need to
```
$ ml amber/22-cpeGNU-23.12-ambertools-22
```

To check for other available versions of Amber, you can use

```
$ module avail amber
```

!!! note

    Note that you need to load the `PDC` module before loading the amber module

This will append the directory containing all Amber executables to your PATH
variable, and set various library paths.
Many of the Amber subprograms come in serial, parallel and other versions,
including:
* `sander`, `sander.MPI`, `sander.LES`, `sander.LES.MPI`
* `pmemd`, `pmemd.MPI`
* `cpptraj`, `cpptraj.MPI`
* `MMPBSA.py`, `MMPBSA.py.MPI`
Here is an example batch script for a parallel execution of ``pmemd.MPI``:
:language: text
For running subprograms that rely on the Python interface to Amber,
for example MMPBSA, one needs to load the appropriate Anaconda Python
distributions and activate the mpi4py conda environment.

# Here is an example batch script for a parallel execution of ``MMPBSA.py.MPI``:

```
#!/bin/bash -l

# Name of you allocation
#SBATCH -A XXXX-XX-XX
# Name of the job
#SBATCH -J myjob
# Partition
#SBATCH -p main
# Maximum wallclock time of job
#SBATCH -t 02:00:00
# Total number of nodes
#SBATCH --nodes=2
# Number of MPI processes per node
#SBATCH --ntasks-per-node=16
module load amber/22-cpeGNU-23.12-ambertools-22
# we run on two nodes with 16 cores per node
srun pmemd.MPI -O -i input.in -o output.out -p prm.prmtop -c coords.rst -r restart.rst -x traj.mdcrd
```
## 

```
#!/bin/bash -l

# Name of you allocation
#SBATCH -A XXXX-XX-XX
# Name of the job
#SBATCH -J myjob
# Maximum wallclock time of job
#SBATCH -t 02:00:00
# Partition
#SBATCH -p main
# Total number of nodes
#SBATCH --nodes=2
# Number of MPI processes per node
#SBATCH --ntasks-per-node=32
module load amber/22-cpeGNU-23.12-ambertools-22
# MMGBSA calculation of a previously generated trajectory
srun MMPBSA.py.MPI -O -i MMPBSA.in -o MMPBSA.dat -sp solvated.prmtop -cp complex.prmtop -rp receptor.prmtop -lp ligand.prmtop -y trajectory.nc >& MMPBSA.log
```
