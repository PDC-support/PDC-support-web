

# Installing software using Spack

Spack is a package manager for supercomputers. It can be used for installing scientific software and libraries for your own software development project in an easy way.

Below you can find short information on how to use spack at PDC, but the full documentation
for spack is available online at [https://spack.readthedocs.io/en/latest/index.html](https://spack.readthedocs.io/en/latest/index.html)

Please note that while there is a central Spack installation used by PDC staff to install software in `/pdc/software/...`, you cannot use this yourself to install software as it is write-protected. The Spack philosophy of working is instead that you work with your own Spack installation
yourself in your private space. It is possible to link your own installation to the PDC central one and reduce the number of package you need to compile by using the so-called “chaining” functionality, see more information here [https://spack.readthedocs.io/en/latest/chain.html](https://spack.readthedocs.io/en/latest/chain.html).

## Setting the environment

This module will facilitate the installation of the desired software
into your home folder and will build software and modules into
 *~/.local/spack/* by default.
If you would like to store your easybuild installation elsewhere please
set its environment variable prior of loading the **spack-user** module.

```default
export SPACK_USER_PREFIX=<MyPath>
```

To activate **spack-user**.

```default
ml PDC/23.12
ml spack-user/0.21.2
```

## Finding and listing available software

If you would like to find out what software you can install, use the `list` command:

```default
$ spack list kokkos
==> 6 packages.
kokkos  kokkos-kernels  kokkos-kernels-legacy  kokkos-legacy  kokkos-nvcc-wrapper  py-pykokkos-base
```

More details about a specific packages, such as configuration flags and build options can be seen with `spack info`

```default
$ spack info kokkos
$ spack info kokkos
CMakePackage:   kokkos

Description:
    Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms.

Homepage: https://github.com/kokkos/kokkos

Maintainers: @DavidPoliakoff @jciesko

Externally Detectable:
    False

Tags:
    e4s

Preferred version:
    3.4.01     https://github.com/kokkos/kokkos/archive/3.4.01.tar.gz
...
```

## Installing software using spack

Installing software using spack in the most basic way is simply:

```default
spack install <software>
```

If there are other packages or libraries that needs to be installed for this software to work, they are also installed automatically. In general, though, you would like to be more specific, and request a certain version of a software, or maybe a specific compiler to be used. There is a specific syntax for doing that:

| Command   | Option                       |
|-----------|------------------------------|
| @         | Which version to install/use |
| %         | Which compiler to use        |
| ^         | Add a specific dependency    |

This is an example of an installation of Amber 18
where it is compiled with GCC version 9.3.0 and a specific ncurses package

```default
spack install amber@18%gcc@9.3.0^ncurses@6.2
...
==> amber: Successfully installed amber-18-js3n7jolbdh7gknbfuiwf5vutoaljckd
Fetch: 1.09s.  Build: 46.92s.  Total: 48.01s.
[+] $HOME/spack/opt/spack/cray-sles15-zen2/gcc-9.3.0/amber-18-js3n7jolbdh7gknbfuiwf5vutoaljckd
```

It is often useful to do a dry run before installing to see what Spack thinks it needs to install. This can be done with `spec` command. For example, what will happen when we request LINPACK?

```default
$ spack spec -I hpl
Input spec
--------------------------------
-   hpl

Concretized
--------------------------------
-   hpl@2.3%gcc@11.2.0~openmp arch=cray-sles15-zen2
[+]      ^cray-libsci@21.08.1.2%gcc@11.2.0~mpi~openmp+shared arch=cray-sles15-zen2
[+]      ^mpich@8.1.11%gcc@11.2.0~argobots+fortran+hwloc+hydra+libxml2+pci+romio~slurm~two_level_namespace~verbs+wrapperrpath device=ch4 netmod=ofi pmi=pmi arch=cray-sles15-zen2
```

Here Spack will compile and install LINPACK using gcc version 11.2.0, MPICH for MPI, and Cray’s LibSci for BLAS and LAPCK. Only the LINPACK package itself will be compiled. Cray Libsci and MPICH are already installed, as indicated by the `[+]` symbols at the beginning of the lines.

## Installing non downloadable software

In some cases it is not possible to directly download the software you are interested in
as the software is restricted by license or other.

In this case you have to download it manually and create folder for it.
See instructions at [https://spack.readthedocs.io/en/latest/basic_usage.html#non-downloadable-tarballs](https://spack.readthedocs.io/en/latest/basic_usage.html#non-downloadable-tarballs)

## Garbage collection

Installing and uninstalling softwares will in the end use up your disk space
so it is good practice to do some garbage collection

```default
spack gc
```

## How to execute your software

Software installed by Spack are put in the directory `spack/opt/spack/cray-sles15-zen2/<compiler>/<software>`.
This can be a bit tedious to use every time, so there are two ways to make it more convenient. Spack automatically makes module files for all installed software, which shows up when you do `module avail`, provided that you can run the Spack initilization script mentioned above. You can then use the `module load` command in the way as you would do for other software at PDC, but in this case you load a software from your own Spack installation.

```default
$ module avail hpl

--------------------------- /cfs/klemming/scratch/y/ypetla/spack/spack/share/spack/modules/cray-sles15-zen2 ---------------------------
hpl-2.3-gcc-11.2.0-5v2u3sq
```

Alternatively, you can use Spack’s built-in mechanism for loading software packages, which works similarily to `module load`:

```default
$ spack load hpl
$ which xhpl
/cfs/klemming/pdc/software/dardel/21.11/spack/spack/opt/spack/cray-sles15-zen2/gcc-11.2.0/hpl-2.3-5v2u3sqa3huu2djhxdtjxbfaoysdwfpy/bin/xhpl
```

…and the software will be directly available via your command line.
