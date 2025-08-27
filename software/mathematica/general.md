Mathematica is an application for scientific calculation and visualization featuring a number of different tools for mathematics, algorithms and data handling.
**Mathematica is licensed software. In order to use Mathematica you need a license.**

# External links
- [Wolfram Mathematica website](http://http://www.wolfram.com/mathematica/)
- [Wolfram learning resources](https://www.wolfram.com/wolfram-u)
- [Mathematica 15-minute video tutorial](https://wolfram.com/wolfram-u/courses/wolfram-language/hands-on-start-to-mathematica-wl005/)
- [Mathematica online course with live Q&A](https://www.wolfram.com/wolfram-u/courses/wolfram-language/mathematica-training-tutorials-hos)

## How to use

Mathematica can be accessed by loading the appropriate module. To see which versions of Mathematica are available use the command
```
ml PDC/<version>
ml spider mathemmatica
ml avail mathematica
# To view info on the module
ml show mathematica
# To load the module
ml mathematica
```
In order to use Mathematica you need to have a Mathematica license. KTH has a site license for KTH users, the server is
mathematica-lic.ug.kth.se
In order to access the installation of Mathematica on Dardel, please contact PDC support and request access.
When you run mathematica for the first time it needs to be activated by pointing it at the license server.

# Running interactively
Mathematica can be run interactively on an allocated node or on cores allocated on a shared node. To book a
single node for one hour, type
```
salloc -N 1 -t 1:00:00 -A pdc.staff -p main
# wait for a node to be reserved
```
A typical output will look like
```
salloc: Granted job allocation 591571
salloc: Waiting for resource configuration
salloc: Nodes nid001015 are ready for job
```
Node nid001015 is now yours for the next hour, and you can log into it and
start Mathematica. On Dardel you can login to the reserved node via the login node
```
ssh -X nid001015
```
and then start Mathematica with
```
ml PDC/<version>
ml mathematica/14.0.0
mathematica
```
For more recent versions of Mathematica, the GUI can be started with `wolframnb`.

In case you do not need a full node with 128 cores, you could request
cores in the shared partition. These cores are shared with other users,
with the amount of memory provided proportional to the number of cores
awarded.
```
salloc -n 24 -t 1:00:00 -A pdc.staff -p shared
```

## Running parallel batch jobs
You can also submit parallel workflows to the SLURM queueing system.
The following job script allocates 16 cores on Dardel and runs one Mathematica
program.
```
#!/bin/bash

#SBATCH -A pdc.staff
#SBATCH -J ker
#SBATCH -t 01:00:00
#SBATCH -p shared
#SBATCH -c 16

# load the Mathematica module
ml PDC/23.12
ml mathematica/14.0.0

# Run Mathematica with the text script <routine name>.m
math -script ker.m

```
Mathematica will parallelize the computation over different cores of the node.
Update the SLURM directives to set your project ID and
the number of nodes and hours that you wish to allocate,
and save the script as ``jobscriptMathematica.sh``.
You can then submit the job with
```
sbatch jobscriptMathematica.sh
```
