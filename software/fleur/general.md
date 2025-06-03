FLEUR is a feature-full, freely available FLAPW (full-potential linearized augmented planewave) code, based on density-functional theory. More information at [https://www.flapw.de](https://www.flapw.de/).

The FLEUR module can be loaded with

```
ml PDC/<version>
ml fleur/max7.0-cpeGNU-24.11
```
FLEUR input files are prepared in two steps. The first step is to prepare an input file containing the basic structural input for the system. The second step is to feed this input file to the input generator executable inpgen which then will produce the full set of FLEUR input files needed in order to run the main FLEUR executable fleur_MPI.

As an example, the basic structural input for Si crystal can read as
```
alpha Si

&input film=f /

&lattice latsys='cF' a0=2.67247737973 a=3.86709 /

2
14  0.125  0.125  0.125
14 -0.125 -0.125 -0.125

&kpt div1=3 div2=3 div3=3 tkb=0.0005 /
```
To run a FLEUR calculation as a batch job, the following example script will run first inpgen and then fleur_MPI.
```
#!/bin/bash
#SBATCH -A naissYYYY-X-XX
#SBATCH -J fleurjob
#SBATCH -p main
#SBATCH -N 1
#SBATCH --ntasks-per-node=128
#SBATCH -t 00:10:00

ml PDC/24.11
ml fleur/max7.0-cpeGNU-24.11

# Run first the input generator
srun -n 1 inpgen -f input.file > inpgen.log

# Run the parallel version of FLEUR
srun fleur_MPI > out.log
```
For reference see the FLEUR [user guide and tutorials](https://www.flapw.de/MaX-7.0/documentation/userGuideOverview).
