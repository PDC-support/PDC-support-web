

# Compilers and libraries

## The Cray Programming Environment

The Cray Programming Environment (CPE) provides consistent interface to multiple compilers and libraries.
On Dardel you can load the `cpe` module to enable a specific version of the CPE. For example

```text
module load cpe/24.11
```

The `cpe` module will make sure that the corresponding versions of several other Cray libraries are loaded,
such as `cray-libsci` and `cray-mpich`. You can check the details by `module show cpe/24.11`.

In addition to the `cpe` module, there are also the `PrgEnv-` modules that provide compilers for
different programming environment

- `PrgEnv-cray`: loads the Cray compiling environment (CCE) that provides compilers for Cray systems.
- `PrgEnv-gnu`: loads the GNU compiler suite.
- `PrgEnv-aocc`: loads the AMD AOCC compilers.

By default the `PrgEnv-cray` is loaded upon login. You can switch to different compilers using
`module swap`:

```text
module swap PrgEnv-cray PrgEnv-gnu
module swap PrgEnv-gnu PrgEnv-aocc
```

## Compiler wrappers

After loading the `cpe` and the `PrgEnv-` modules, you can now build your parallel applications
using compiler wrappers for C, C++ and Fortran:

```text
cc -o myexe.x mycode.c      # cc is the wrapper for C compiler
CC -o myexe.x mycode.cpp    # CC is the wrapper for C++ compiler
ftn -o myexe.x mycode.f90   # ftn is the wrapper for Fortran compiler
```

The compiler wrappers will choose the required compiler version, target architecture options, and will automatically
link to the scientific libraries, as well as the MPI and OpenSHMEM libraries.
No additional MPI flags are needed as these are included by compiler wrappers, and
there is no need to add any `-I`, `-l` or `-L` flags for the Cray provided libraries.
For libraries and include files covered by module files, you need not add anything to your Makefile.
If a Makefile needs an input for -L to work correctly, try using “`.`”.

For code development, testing, and performance analysis, it is good practice to build code with two different tool chains.
On Dardel a starting point is to use the `PrgEnv-cray` and the `PrgEnv-gnu` environments.

## Cray scientific and math libraries

The Cray scientific and math libraries (CSML) provide the `cray-libsci` and `cray-fftw` modules
that are designed to provide optimial performance from Cray systems.

- `cray-libsci`: provides BLAS, LAPACK, ScaLAPACK, etc.
- `cray-fftw`: provides fastest fourier transform.

The `cray-libsci` module supports OpenMP and the number of threads can be controlled by the
`OMP_NUM_THREADS` environment variable.

The `cray-libsci` module is loaded upon login, and its version can be changed by the `cpe` module.
The `cray-fftw` module needs to be loaded by user.

## Cray message passing toolkit

The Cray message passing toolkit (CMPT) provides the `cray-mpich` module, which is based on ANL
MPICH and has been optimized for Cray programming environment.

The `cray-mpich` module is loaded upon login, and its version can be changed by the `cpe` module.
Once `cray-mpich` is loaded the compiler wrapper will automatically include MPI headers and link to
MPI libraries.

If you would like to use SHMEM you can check the availability of the `cray-openshmemx` module by
“`module avail cray-openshmemx`”.

## Compiler and linker flags

Verbose printing of the flags and settings that are active when using the compiler wrappers

```text
-craype-verbose
```

A suggested starting point for code optimization on AMD EPYC Zen 2 processors are

* for the **Cray** compilers

```text
# C C++ flags
-Ofast              # Aggresive optimization
-flto               # link time optimization
-ffp=3              # optimization of floating-point math operations. Supported values are 0, 1, 2, 3, and 4.
-fcray-mallopt      # use Cray's mallopt parameters, can improve performance
-fno-cray-mallopt   # no use of Cray's mallopt parameters, can reduce memory usage
-fopenmp            # enable OpenMP

# Fortran flags
-02                 # default optimization
-O3                 # aggresive optimization
-O ipaN             # level of inline expansion N=0-5, default N=3
-hlist=a            # write optimization info to listing file
-hlist=a            # create source listing with loopmark information
-homp               # enable OpenMP
-hthread            # level of optimization of OpenMP directive, N=0-3, default N=2
```

* for the **GCC** compilers

```text
# General flags

# C C++  Fortran flags
-O3                 # aggresive optimization
-march=znver2       # name of the target architecture
-mtune=znver2       # name of the target processor for which code performance will be tuned
-mfma               # enable fma instructions
-mavx2              # enable avx2 instructions
-m3dnow             # enable 3dnow instructions
-fomit-frame-pointer  # omit the frame pointer in functions that do not need one
-fopenmp            # enable OpenMP

# Fortran flags
-std=legacy         # specify legacy Fortran standard
-fallow-argument-mismatch  # allow for mismatches between calls and procedure definitions
```

* for the **AOCC** compilers

```text
# C C++ Fortran flags
-02                 # default optimization
-O3                 # aggresive optimization
-O ipaN             # level of inline expansion N=0-5, default N=3
-flto               # link time optimization
-funroll-loops      # loop unrolling
-unroll-aggressive  # advance loop optimization
-fopenmp            # enable OpenMP

# Fortran flags
-ffree-form         # support for free form Fortran
```

## Build examples

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
# returns Cray Fortran   Version 17 0 0

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
# Lmod is automatically replacing "cpeGNU/24.11" with "PrgEnv-gnu/8.5.0" 
# Lmod is automatically replacing "cce/17.0.0" with "gcc/12.3" 
# Lmod is automatically replacing "PrgEnv cray 8 5 0" with "cpeGNU/24.11" 
# Due to MODULEPATH changes  the following have been reloaded 
# 1  cray-libsci/24.11.0    2  cray-mpich/8.1.28

# Check which compiler the cc compiler wrapper is pointing to
cc --version
gcc-12 (SUSE Linux) 12.3.0

ml list
# The listing reveals that cray-libsci/24.11.0 is already loaded 

# In addition  the program needs linking also to a Fourier transform library 
ml spider fftw
# gives a listing of available Fourier transform libraries 
# Load a recent version of the Cray FFTW library with
module add cray-fftw/3.3.10.6

# Build the code with
cc fftw_test.c -o fftw_test.x

# Test the code in interactive session 
# First queue to get one reserved core for 10 minutes
salloc -n 1 -t 0:10:00 -A <project name> -p shared
# wait for the core  Then run the program with
srun -n 1 ./fftw_test.x
```

Having loaded the cray-fftw module, no additional linking flag(s) was needed for the **cc** compiler wrapper.

**Example 3:** Build a program with the EasyBuild cpeGNU/24.11 toolchain

```text
# Load an EasyBuild user module
ml PDC/24.11
ml easybuild-user

# Look for a recipe for the Libxc library
eb -S Libxc
# Returns a list of available EasyBuild easyconfig files 
# Choose an easyconfig file for the cpeGNU 24.11 toolchain 

# Make a dry run
eb libxc-7.0.0-cpeGNU-24.11.eb --robot --dry-run

# Check if dry run looks reasonable  Then proceed to build with
eb libxc-7.0.0-cpeGNU-24.11.eb --robot

# The program is now locally installed in the user s
# ~  local easybuild directory and can be loaded with
ml PDC/24.11
ml easybuild-user
ml libxc-7.0.0-cpeGNU-24.11.eb
```
