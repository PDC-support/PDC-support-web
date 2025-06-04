

# Quick Start

## Brief description

You can find documentation on our clusters at [https://www.pdc.kth.se/hpc-services/computing-systems](https://www.pdc.kth.se/hpc-services/computing-systems)

## How to log in

In order to be able to login into PDC system, you need a PDC account linked with your [SUPR](https://supr.naiss.se/) account.

1. First follow the instructions on how to generate an SSH key pair, see [Generating SSH keys](../login/ssh_keys.md).
1. Goto [PDC login portal](https://loginportal.pdc.kth.se/) and follow instructions.
1. Login to PDC resources
   ```text
   ssh <user name>@dardel.pdc.kth.se
   ```

For more details on how to log in, see [How to log in with SSH keys](../login/ssh_login.md).

In case you do not have a SUPR account you can also [How to log in with kerberos](../login/kerberos_login.md)

## Storage

The user home directories, project directories, and scratch file area are stored on a Lustre file system which is mounted to the Dardel compute and login nodes.

The home directories have a quota of 25 GB.

The project directories are not backed up. **You are advised to always move data, and keep additional copies of the most important input and output files**.

The scratch area is intended for temporary large files that are used during calculations. **The scratch area is automatically cleaned by removing files that has not been changed within a certain time.** **You are advised to always move data, and keep additional copies of the most important input and output files**.

For more details on storage, see [Storage areas](../data_management/klemming.md).

## Transfer of files

Files and directories can be transferred to and from Dardel with the rsync or scp command.

```text
# To transfer a file from local computer to Dardel
rsync localfile <user name>@dardel.pdc.kth.se:<directory>/.
# To transfer a file from Dardel to local computer
scp <user name>@dardel.pdc.kth.se:<directory>/<file> .
```

For more details on how to transfer files, see [Using rsync/scp](../data_management/file_transfer.md).

## The Lmod module system

Dardel uses the Lmod environment module system. Lmod allows for the dynamic adding and removal of installed software packages to the running environment. To access, list and search among the installed application programs, libraries, and tools, use the *module* command (or the shortcut *ml*)

```text
ml
# lists the loaded software modules

ml avail
# lists the available software modules

ml avail <program name>
# lists the available versions of a given software
```

Many softwares are not directly available using the above command as they are built within different Cray programming environments.
To find all software and all its dependencies.

```text
ml spider <program name>
# lists the available versions of a given software and what dependent modules need to be loaded
```

When you have found the program you are looking for, use

```text
ml <program>
# to load the program module
```

Many software modules become available after loading the latest `PDC` module.

```text
ml PDC
```

For more details on how to use modules, see [How to use module to load different softwares into your environment](../software/module.md).

## The Cray programming environment

The Cray Programming Environment (CPE) provides a consistent interface to multiple compilers and libraries.
On Dardel you can load the `cpe` module to enable a specific version of the CPE. For example

```text
ml cpe/24.11
```

In addition to the `cpe` module, there are also the `PrgEnv-` modules that provide compilers for
different programming environment

- `PrgEnv-cray`: loads the Cray compiling environment (CCE) that provides compilers for Cray systems.
- `PrgEnv-gnu`: loads the GNU compiler suite.
- `PrgEnv-aocc`: loads the AMD AOCC compilers.

By default the `PrgEnv-cray` is loaded upon login. You can switch to different compilers by
loading another `PrgEnv-` module

```text
ml PrgEnv-gnu
ml PrgEnv-aocc
```

After loading the `cpe` and the `PrgEnv-` modules, you can now build your parallel applications
using compiler wrappers for C, C++ and Fortran

```text
cc -o myexe.x mycode.c      # cc is the wrapper for C compiler
CC -o myexe.x mycode.cpp    # CC is the wrapper for C++ compiler
ftn -o myexe.x mycode.f90   # ftn is the wrapper for Fortran compiler
```

The compiler wrappers will choose the required compiler version, target architecture options, and will automatically
link to the math and MPI libraries.
There is no need to add any `-I`, `-l` or `-L` flags for the Cray-provided libraries.

- Math libraries:

  There are the `cray-libsci` and `cray-fftw` modules
  that are designed to provide optimal performance from Cray systems.  The
  `cray-libsci` module provides BLAS/LAPACK/ScaLAPACK and supports OpenMP.
  The number of threads can be controlled by the `OMP_NUM_THREADS`
  environment variable.
- MPI library:

  There is the `cray-mpich` module, which is based on ANL
  MPICH and has been optimized for Cray programming environment.

All softwares at PDC are installed using a specific CPE. The software installed using the latest CPE can be accessed by

```text
ml PDC
```

The `PDC` modules are directly related to the CPE version and
a number of older software modules can also be viewed by looking at older `PDC` modules.

## Build your first program

**Example 1:** Build an MPI parallelized Fortran code within the PrgEnv-cray environment

In this example we build and test run a Hello World code `hello_world_mpi.f90`.

```text
program hello_world_mpi
include "mpif.h"
integer myrank,size,ierr
call MPI_Init(ierr)
call MPI_Comm_rank(MPI_COMM_WORLD,myrank,ierr)
call MPI_Comm_size(MPI_COMM_WORLD,size,ierr)
write(*,*) "Processor ",myrank," of ",size,": Hello World!"
call MPI_Finalize(ierr)
end program
```

The build is done within the PrgEnv-cray environment using the Cray Fortran compiler, and the testing is done on a Dardel CPU node reserved for interactive use.

```text
# Check which compiler the compiler wrapper is pointing to
ftn --version
# returns Cray Fortran : Version 18.0.1

# Compile the code
ftn hello_world_mpi.f90 -o hello_world_mpi.x

# Test the code in interactive session
# First queue to get one node reserved for 10 minutes
salloc -N 1 -t 0:10:00 -A <project name> -p main
# wait for the node  Then run the program using 128 MPI ranks with
srun -n 128 ./hello_world_mpi.x
# with program output to standard out
#
# Processor  123  of  128   Hello World
#
# Processor  47  of  128   Hello World
#
```

Having here used the **ftn** compiler wrapper, the linking to the cray-mpich library was done without the need to specify linking flags. As is expected for this code, in runtime each MPI rank is writing its Hello World to standard output **without** any synchronization with the other ranks.

**Example 2:** Build a C code with PrgEnv-gnu. The code requires linking to a Fourier transform library.

```text
# Download a C program that illustrates use of the FFTW library
mkdir fftw_test
cd fftw_test
wget https://people.math.sc.edu/Burkardt/c_src/fftw/fftw_test.c

# Change from the PrgEnv cray to the PrgEnv gnu environment
ml PDC/24.11
ml cpeGNU/24.11
#Lmod is automatically replacing "cpeGNU/24.11" with "PrgEnv-gnu/8.6.0".
#Lmod is automatically replacing "cce/18.0.1" with "gcc-native/12.3".
#Lmod is automatically replacing "PrgEnv-cray/8.6.0" with "cpeGNU/24.11".
#Due to MODULEPATH changes, the following have been reloaded:
#  1) cray-libsci/24.11.0     2) cray-mpich/8.1.31

# Check which compiler the cc compiler wrapper is pointing to
cc --version
# gcc-12 (SUSE Linux) 12.3.0

ml
# The listing reveals that cray-libsci/24.11.0 is already loaded

# In addition  the program needs linking also to a Fourier transform library
ml spider fftw
# gives a listing of available Fourier transform libraries
# Load a recent version of the Cray FFTW library with
ml cray-fftw/3.3.10.9

# Build the code with
cc fftw_test.c -o fftw_test.x

# Test the code in interactive session
# First queue to get one reserved core for 10 minutes
salloc -n 1 -t 0:10:00 -A <project name> -p shared
# wait for the core  Then run the program with
srun -n 1 ./fftw_test.x
```

Having loaded the cray-fftw module, no additional linking flag(s) was needed for the **cc** compiler wrapper.

**Example 3:** Build a program with the EasyBuild cpeGNU/21.09 toolchain

```text
# Load an EasyBuild user module
ml PDC/24.11
ml easybuild-user/4.9.4

# Look for a recipe for the Libxc library
eb -S libxc
# Returns a list of available EasyBuild easyconfig files
# Choose an easyconfig file for the cpeGNU 23 12 toolchain

# Make a dry run
eb libxc-6.2.2-cpeGNU-24.11.eb --robot --dry-run

# Check if dry run looks reasonable  Then proceed to build with
eb libxc-6.2.2-cpeGNU-24.11.eb --robot

# The program is now locally installed in the user's
# ~/.local/easybuild directory and can be loaded with
ml PDC/24.11
ml easybuild-user/4.9.4
ml libxc/6.2.2-cpeGNU-24.11
```

## How to use EasyBuild

At PDC we have EasyBuild installed to simplify the installation of HPC software and
several **easyconfig** software recipes are available via the command line.
In order to use EasyBuild in your local folder

```text
ml PDC/24.11
ml easybuild-user/4.9.4
```

EasyBuild installed software will build into  *~/.local/easybuild* folder and
are automatically available as modules.

For more information regarding how to EasyBuild at PDC go to [Installing software using EasyBuild](../software_development/easybuild.md)

## Submit a batch job to the queue

PDC uses the Slurm Workload Manager to schedule jobs.

You are advised to always submit jobs from a directory within the **project** and **scratch** partitions of the file system.

Keep additional copies of **the most important input and output** files in your home directory.

The Dardel CPU nodes have 128 cores. Please note that if you request a full node, your project allocation will be
charged for use of 128 cores, even if your program uses a smaller number of cores. You are advised to submit
jobs that will use fewer cores than 128 to the **shared** partion.

For more details on the partition, see [Dardel partitions](../run_jobs/job_scheduling.md#dardel-partitions).

**Example 1:** Submit an batch job to run on 64 cores of a node that is shared with other jobs.

In this example we will run a batch job for the `hello_world_mpi.f90` code. To this end, we prepare a *jobscript.sh*

```text
#!/bin/bash
# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A <project name>
# The name of the script is myjob
#SBATCH -J myjob
# 10 minutes wall clock time will be given to this job
#SBATCH -t 00:10:00
# The partition
#SBATCH -p shared
# The number of tasks requested
#SBATCH -n 64
# The number of cores per task
#SBATCH -c 1

echo "Script initiated at `date` on `hostname`"
srun -n 64 hello_world_mpi.x
echo "Script finished at `date` on `hostname`"
```

The batch job is submitted to the job queue with the `sbatch` command. After submission with

```text
sbatch jobscript.sh
```

The status of the job (pending in queue, running, etc) can be monitored with the *squeue* command.

```text
squeue -u $USER
```

The standard output of the program is written to a file slurm-<job number>.out. We inspect the output

```text
Script initiated at thu oct 28 14:52:26 CEST 2023 on nid001064
..
Processor  25  of  64 : Hello World!
Processor  34  of  64 : Hello World!
..
Script finished at thu oct 28 14:52:28 CEST 2023 on nid001064
```

For more details on how to write batch scripts and submit batch jobs to queues, see [How to Run Jobs](../run_jobs/job_scheduling.md) and [Queueing jobs](../run_jobs/queueing_jobs.md).

**Example 2:** Submit a batch job to queue for a center installed software

In this example we will perform a calculation on two Dardel CPU compute nodes with
the [ABINIT](https://www.abinit.org/) package for modeling of condensed matter.
The example calculation is a density functional theory (DFT) simulation of the properties of the material SrVO3. ABINIT is available as a PDC center installed software, as listed on the page [Available Software](https://support.pdc.kth.se/doc/applications/). Reference information on how to use and build ABINIT on Dardel can be found at [ABINIT](https://support.pdc.kth.se/doc/applications/abinit/).

We activate the ABINIT software module with

```text
ml PDC/24.11
ml abinit/10.2.7-cpeGNU-24.11
```

In order to learn more about what environment variables were set by the *ml* command

```text
ml show abinit/10.2.7-cpeGNU-24.11
# which reveals that
# /pdc/software/24.11/eb/software/abinit/10.2.7-cpeGNU-24.11/bin
# was appended to the PATH
```

In order to set up the simulation for SrVO3 we need an *abi* input file and
a set of pseudopotentials for the chemical elements. These are contained in
the ABINIT 10.2.7 release

Download and extract the ABINIT 10.2.7 release

```text
mkdir ABINIT
cd ABINIT
wget https://www.abinit.org/sites/default/files/packages/abinit-10.2.7.tar.gz
tar xf abinit-10.2.7.tar.gz
# where the files and directories needed for this example are
abinit-10.2.7/tests/tutoparal/Input/tdmft_1.abi
abinit-10.2.7/tests/Psps_for_tests/
```

In order to run the calculation as a batch job on two nodes, prepare a *jobscriptabinit.sh*
where the *your-project-account* should be an active compute project, and *Psps_for_tests*
should be the path to the pseudopotentials.

```text
#! bin bash
# time allocation
#SBATCH -A <your project account>
# name of this job
#SBATCH -J abinit job
# wall time for this job
#SBATCH -t 00:30:00
# number of nodes
#SBATCH --nodes=2
# The partition
#SBATCH -p main
# number of MPI processes per node
#SBATCH --ntasks-per-node=128

ml PDC/24.11
ml abinit/10.2.7-cpeGNU-24.11

export ABI_PSPDIR=<Psps_for_tests>

echo "Script initiated at `date` on `hostname`"
srun -n 256 abinit tdmft_1.abi > out.log
echo "Script finished at `date` on `hostname`"
```

The batch job is submitted to the job queue with the *sbatch* command

```text
sbatch jobscriptabinit.sh
```

The status of the job (pending in queue, running, etc) can be monitored with the *squeue* command.

```text
squeue -u $USER
```

The standard output of the program was directed to the file out.log.
We inspect the last 20 lines of the output

```text
tail -n 20 out.log
# which prints
--- !FinalSummary
program: abinit
version: 9.10.3
start_datetime: Wed Mar 13 13:06:53 2024
end_datetime: Wed Mar 13 13:07:03 2024
overall_cpu_time: 2631.2 s
overall_wall_time: 2691.9 s
exit_requested_by_user: no
timelimit: 0
pseudos:
    V   : e583d1cc132dd79ce204b31204bd83ed
    Sr  : 02b29cc3441fa9ed5e1433b119e79fbc
    O   : c8ba4c11dba269a1224b8b74498fed92
usepaw: 1
mpi_procs: 256
omp_threads: 1
num_warnings: 1
num_comments: 0
...
```

**Exercise** The final summary states one warning. Search in
*out.log* for warning messages. What do they indicate on the matching
of hardware requested for the job, and the problem size?

More details on this particular example can be found in the ABINIT [tutorial on DFT+DMFT](https://docs.abinit.org/tutorial/dmft/).

## References

[Dardel HPE Cray EX supercomputer at PDC](https://www.pdc.kth.se/hpc-services/computing-systems/){:target="_blank"}

[PDC Available Software](https://www.pdc.kth.se/software/){:target="_blank"}

[PDC Support web pages](https://www.pdc.kth.se/support/){:target="_blank"}

[HPE Cray EX product line](https://www.hpe.com/us/en/compute/hpc/supercomputing/cray-exascale-supercomputer.html/){:target="_blank"}

