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
  memory available for each MPI rank. For VASP versions that have shared memory parallelization
  implemented with OpenMP threading, you can use more than one thread per MPI rank.

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
Since OpenMP is supported by VASP 6.4.3, you can also submit a job
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

## How to build VASP
These are the steps which were used to build the module `vasp/6.5.1-vanilla`.

### Obtain and unpack the VASP source code
```
tar xf vasp.6.5.1.tgz
cd vasp.6.5.1
```

### Apply readonly-patch
In order to lower the footprint on the file system in runtime, apply before compiling the readonly-patch
```
--- src/pseudo.F	2025-03-10 16:41:26.000000000 +0100
+++ src/pseudo_new.F	2025-05-05 08:57:54.000000000 +0200
@@ -233,7 +233,7 @@
 !        END IF
       END IF
 #endif
-      OPEN(UNIT=10,FILE=DIR_APP(1:DIR_LEN)//'POTCAR',STATUS='OLD',IOSTAT=IERR)
+      OPEN(UNIT=10,FILE=DIR_APP(1:DIR_LEN)//'POTCAR',ACTION='READ',STATUS='OLD',IOSTAT=IERR)
       IF (IERR/=0) THEN
          OPEN(UNIT=10,FILE='POTCAR',STATUS='OLD')
       ENDIF
--- src/string.F	2025-03-10 16:41:27.000000000 +0100
+++ src/string_new.F	2025-05-05 08:58:56.000000000 +0200
@@ -94,7 +94,7 @@
         integer, intent(out) :: ierr  !< error flag that will be set if accessing the file fails
         character(len=:), allocatable :: content
         integer file_unit
-        open(newunit=file_unit,file=filename,status='old',form='unformatted',access='stream',iostat=ierr)
+        open(newunit=file_unit,file=filename,status='old',form='unformatted',access='stream',action='read',iostat=ierr)
```
by storing the patch to file name `POTCAR-readonly-651.patch` and applying it with the patch command
```
patch -p0 -b < POTCAR-readonly-651.patch
```

### Configure the VASP makefile.include

Configure the `makefile.include` file as needed. For the globally installed VASP modules the
file can be found in the directory `$VASPROOT/example-files`. Here are the settings used for
the `vasp/6.5.1-vanilla` module.
```
# Default precompiler options
CPP_OPTIONS = -DHOST=\"Dardel\" \
              -DMPI -DMPI_BLOCK=65536 -Duse_collective \
              -DscaLAPACK \
              -DCACHE_SIZE=65536 \
              -Davoidalloc \
              -Dvasp6 \
              -Dtbdyn \
              -Dfock_dblbuf \
              -D_OPENMP -DnoSTOPCAR

CPP         = cc -E -C -w $*$(FUFFIX) >$*$(SUFFIX) $(CPP_OPTIONS)

FC          = ftn -fopenmp
FCL         = ftn -fopenmp

FREE        = -ffree-form -ffree-line-length-none

FFLAGS      = -w -ffpe-summary=none

OFLAG       = -O2
OFLAG_IN    = $(OFLAG)
DEBUG       = -O0

# For what used to be vasp.5.lib
CPP_LIB     = $(CPP)
FC_LIB      = $(FC)
CC_LIB      = cc
CFLAGS_LIB  = -O
FFLAGS_LIB  = -O1
FREE_LIB    = $(FREE)

OBJECTS_LIB = linpack_double.o

# For the parser library
CXX_PARS    = CC
LLIBS       = -lstdc++

##
## Customize as of this point! Of course you may change the preceding
## part of this file as well if you like, but it should rarely be
## necessary ...
##

# When compiling on the target machine itself, change this to the
# relevant target when cross-compiling for another architecture
#VASP_TARGET_CPU ?= -march=native
#FFLAGS     += $(VASP_TARGET_CPU)

# For gcc-10 and higher (comment out for older versions)
FFLAGS     += -fallow-argument-mismatch

# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
#BLASPACK    = -L$(OPENBLAS_ROOT)/lib -lopenblas

# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
#SCALAPACK   = -L$(SCALAPACK_ROOT)/lib -lscalapack

#LLIBS      += $(SCALAPACK) $(BLASPACK)

# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
#LLIBS      += -L$(FFTW_ROOT)/lib -lfftw3 -lfftw3_omp
#INCS       += -I$(FFTW_ROOT)/include

# HDF5-support (optional but strongly recommended, and mandatory for some features)
#CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
#LLIBS      += -L$(HDF5_ROOT)/lib -lhdf5_fortran
#INCS       += -I$(HDF5_ROOT)/include

# For the VASP-2-Wannier90 interface (optional)
#CPP_OPTIONS    += -DVASP2WANNIER90
#WANNIER90_ROOT ?= /path/to/your/wannier90/installation
#LLIBS          += -L$(WANNIER90_ROOT)/lib -lwannier

# For the fftlib library (recommended)
#CPP_OPTIONS+= -Dsysv
#FCL        += fftlib.o
#CXX_FFTLIB  = CC -fopenmp -std=c++11 -DFFTLIB_THREADSAFE
#INCS_FFTLIB = -I./include -I$(FFTW_ROOT)/include
#LIBS       += fftlib
#LLIBS      += -ldl

# For machine learning library vaspml (experimental)
#CPP_OPTIONS += -Dlibvaspml
#CPP_OPTIONS += -DVASPML_USE_CBLAS
#CPP_OPTIONS += -DVASPML_DEBUG_LEVEL=3
#CXX_ML      = mpic++ -fopenmp
#CXXFLAGS_ML = -O3 -std=c++17 -pedantic-errors -Wall -Wextra
#INCLUDE_ML  = -I$(OPENBLAS_ROOT)/include
```

### Load the build environment, Gnu toolchain
```
ml PDC/24.11
ml cpeGNU/24.11
ml cray-fftw/3.3.10.9
```

### Build the VASP executables
```
make
```

### Create symbolic links for the executables
```
cd bin
ln -s vasp_std vasp
ln -s vasp_ncl vasp_noncollinear
ln -s vasp_gam vasp_gamma
```
