The University of Oregon’s TAU is an open-source portable profiling and tracing toolkit for the performance analysis of parallel programs written in Fortran, C, C++, UPC, Java, Python and other languages. The instrumentation of programs can be done by binary code rewriting, manual compiler directives, or automatic source code transformation. TAU can support many parallel programming interfaces, including MPI, OpenMP, pthreads, and ROCm. TAU includes paraprof which is a profile visualization tool, and generated execution traces can be displayed by the Vampir, Paraver or JumpShot (included) visualization tools.

[https://www.cs.uoregon.edu/research/tau/docs.phpx](https://www.cs.uoregon.edu/research/tau/docs.phpx)


## How to use

Load the following modules
```
$ module load PrgEnv-gnu
$ module load PDC
$ module load tau
```
Compile your code using tau wrappers, such as `tau_cc`, `tau_cxx`, `tau_f90`/`tau_f77`. For instance, to compile a `C++` code, the following command can be used:

`tau_cxx.sh <myProgran.cpp> -o <myProgramEx>`


and export the environment variable:

`export PROFILEDIR=<path-to-profiling-data-directory>`
<!--- export TAU_TRACE=1 TAU_PROFILE=1 -->
Then, run the program binary as follows:

`srun <flags-as-usual> tau_exec <binary>`

After the program completes its run successfully, navigate to the profile (`cd $PROFILEDIR`)data directory and run the following command `pprof` to generate a text output, or `paraprof` to generate graphical output.

> **_NOTE:_**  If your program uses OpenMP based parallelism, make sure to use `--hint=nomultithread` along with the srun command

