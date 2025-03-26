

# PDC Summer School

This page contains useful information for the PDC summer school.

## Account and login

Please see instructions for acquiring a PDC account and logging in to
PDC clusters in the [General instructions for PDC courses](general.md).

## Virtual machine

All participants will receive a USB memory stick with an Ubuntu
virtual machine (VM) image which can be used to log in to PDC. To use
the VM, you will need to
[install VirtualBox](https://www.virtualbox.org/wiki/Downloads).
The image can also [be downloaded here](https://kth.box.com/s/rcuktqzzx79ap7bsoubxigl5ogms605a).

Note that you can also use the VM for the Software Engineering and
Singularity lessons, so we recommend all participants to install VirtualBox.

## Compiling code

Dardel have different compiler environments which you will use to compile code
for the lab exercises. Detailed information can be found at [https://www.pdc.kth.se/support/documents/software_development/development_intro.html](https://www.pdc.kth.se/support/documents/software_development/development_intro.html), but a
summary is found below.

**Dardel** uses compiler wrappers so that source code is compiled
with the compiler environment currently loaded. By default the `PrgEnv-cray` module is loaded
when you log in, but you can change to the AMD compiler suite by

```default
$ module swap PrgEnv-cray PrgEnv-aocc
```

and to GNU compilers with

```default
$ module swap PrgEnv-cray PrgEnv-gnu
```

Regardless of which compiler suite is loaded, you should use the same compiler commands
`ftn`, `cc` and `CC` to compile.

Compiling serial and MPI code (note that no MPI flags are needed):

```default
# Fortran
ftn [flags] source.f90
# C
cc [flags] source.c
# C++
CC [flags] source.cpp
```

Compiling OpenMP code:

```default
ftn -homp source.f90
cc -fopenmp source.c
CC -fopenmp source.cpp
```

## Running jobs

After logging in you are on the login node of the cluster. The login node is a shared resource and
should not be used for running parallel jobs. Instead, the SLURM scheduling system should be
used to either run **interactive jobs** or **submit batch jobs** to the queue (see [How to Run Jobs](../run_jobs/job_scheduling.md)).
You can however use the login node to edit files and compile code.

To request compute resources interactively or via a batch job, you need to specify an *allocation ID*, a
*reservation ID*, how much time your job needs and how many nodes it should use.
**To request an interactive node** for 1 hour, run the command

```default
$ salloc -A edu19.summer --reservation <reservation-name> -N 1 -t 1:0:0
```

When the interactive compute node is allocated to you, a new shell session is started (in the same terminal).
To run a parallel job on the interactive node, type:

```default
$ srun -n 32 ./my_executable
```

**To run a batch job**, you first need to prepare a submit script. In the simplest case, it can look like this:

```default
#! bin bash  l
#SBATCH  A edu19 summer
#SBATCH   reservation= reservation name 
#SBATCH  P shared
#SBATCH  J name of my job
#SBATCH  t 1 00 00
#SBATCH  N 2
srun -n 64 ./my_executable > my_output_file 2>&1
```

To submit the job to the scheduler, type

```default
$ sbatch my_submit_script.bash
```

You can then monitor the job using

```default
$ squeue -u <your-username>
```

and if you need to cancel the job, find its job-ID using the `squeue` command and type

```default
$ scancel <job-ID>
```

## File transfer

Files are transferred with scp from PDC to your local machine as follows:

```default
$ scp <username>@dardel.pdc.kth.se:<filename> .
```

or the other way by:

```default
$ scp <filename> <username>@dardel.pdc.kth.se:~/
```

Here is more information on [Using scp/rsync](../data_management/file_transfer_scp.md)

## Lab exercises

### Quick Reference Guide

Check out our quick reference guide to using PDC resources.

### Introduction to PDC

Lecture slides can be found
[here](https://github.com/PDC-support/introduction-to-pdc/blob/summer-school/presentation.pdf).

### Software engineering

All course material, including exercises and installation/preparation steps
to be done before the summer school starts, can be found
[on this page](https://pdc-support.github.io/software-engineering-intro/).

### Singularity

Lecture slides [can be found here](https://gitpitch.com/PDC-support/singularity-introduction#/).

### OpenMP

All exercises can be found in [this GitHub repository](https://github.com/PDC-support/openmp-lab-exercises).
You can either clone it to your computer or navigate the exercises on GitHub.

### CUDA

All exercises can be found in [this GitHub repository](https://github.com/PDC-support/cuda-lab-exercises).
You can either clone it to your computer or navigate the exercises on GitHub.

Instructions for the two sets of exercises:

- Lab 1 [in C](https://github.com/PDC-support/cuda-lab-exercises/blob/master/lab_1/README.md)
  and guidelines for solving the lab [in Fortran](https://github.com/PDC-support/cuda-lab-exercises/blob/master/lab_1/Fortran/README.md).
- Lab 2 [in C](https://github.com/PDC-support/cuda-lab-exercises/blob/master/lab_2/README.md)
  (and use the same guidelines as above for solving it in Fortran).

### MPI

All exercises can be found in [this GitHub repository](https://github.com/PDC-support/mpi-lab-exercises).
You can either clone it to your computer or navigate the exercises on GitHub.

### Performance Engineering

TBD
