

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
