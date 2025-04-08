GROMACS is a versatile package to perform molecular dynamics, i.e. simulate the Newtonian equations of motion for systems with hundreds to millions of particles. It provides extremely high performance through custom algorithmic optimizations. More information on the [GROMACS homepage](https://www.gromacs.org).
Several versions of GROMACS are installed at PDC. Generally, it is recommended to use the most recent version since it can be expected to be faster,
more stable and less memory demanding.
Information on how to run GROMACS on AMD GPU nodes of an HPE Cray EX cluster can be found in [How to run GROMACS efficiently on the LUMI supercomputer](https://zenodo.org/records/10683366).

## How to use

GROMACS is highly tuned for quite efficient use of HPC resources.
Special assembly kernels make its core compute engine one of the fastest MD
simulation programs.

## How to user
You can check for available GROMACS modules with
```
ml spider gromacs
```

For example, to load the module for GROMACS 2024.2/
```
ml PDC/<version>
ml gromacs/2024.2-cpeGNU-23.12
```
To see what environment variables are set when loading the module
```
ml gromacs/2024.2-cpeGNU-23.12
```
Preprocessing input files (molecular topology, initial coordinates and
mdrun parameters) to create a portable run input (.tpr) file can be run
in a batch job by
```
srun -n 1 gmx_mpi grompp -c conf.gro -p topol.top -f grompp.mdp
```
Gromacs also contains a large number of other pre- and post-processing tools.
A list of available commands can be seen by
```
srun -n 1 gmx_mpi help commands
```
The GROMACS module provide up to four main versions of the GROMACS suite
##
- *gmx* : The MD engine binary without MPI, but with openMP threading. Useful if GROMACS is executed for preprocessing or running analysis tools on a compute node.
- *gmx_mpi* : The MD engine binary with MPI support. This is the one that researchers would use most of the time.
- *gmx_d* : Same as *gmx* above but in double precision.
- *gmx_mpi_d* : Same as *gmx_mpi* above but in double precision.

All tools from the GROMACS suite can be launched using any of the above
versions. Please note that they should be launched on the compute node(s).
Remember to *always* use in your scripts *srun* in front of the actual GROMACS
command! Here is an example script that requests 2 nodes:

```
#!/bin/bash

#SBATCH -J my_gmx_job
#SBATCH -A naissYYYY-X-XX
#SBATCH -p main
#SBATCH -t 01:00:00

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128

ml PDC/<version>
ml gromacs/2024.2-cpeGNU-23.12

export OMP_NUM_THREADS=1

srun -n 1 gmx_mpi grompp -c conf.gro -p topol.top -f grompp.mdp
srun gmx_mpi mdrun -s topol.tpr -deffnm gmx_md
```

## How to build GROMACS

The program was installed using [EasyBuild](https://docs.easybuild.io/en/latest/).
A build in your local file space can be done with

```bash
ml PDC/23.12
ml easybuild-user/4.9.1
eb gromacs-2024.2-cpeGNU-23.12.eb --robot
```

See also [Installing software using EasyBuild](https://support.pdc.kth.se/doc/support-docs/software_development/easybuild/).
