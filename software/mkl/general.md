`Intel Math Kernel Library (MKL) <https://software.intel.com/en-us/intel-mkl>`_
is a math library
developed by Intel which provides BLAS, CBLAS, LAPACK, and SCALAPACK.
For linking consult the `math kernel library link line advisor <https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor/>`_.
Also note that when you compile using the Intel compilers, you can avoid
all explicit linking by using the ``-mkl=[parallel,sequential,cluster]`` compiler flag.

## How to use

The flags for a typical situation, using the intel compiler and 32 bit integers are as follows
```
LDFLAGS="-L/pdc/vol/i-compilers/17.0.1/mkl/lib/intel64 -lmkl_intel_lp64 \
-lmkl_sequential -lmkl_core -lpthread \
-Wl,--rpath,/pdc/vol/i-compilers/17.0.1/mkl/lib/intel64"
CFLAGS="-I/pdc/vol/i-compilers/17.0.1/mkl/include"
```
Also note that when you compile using the Intel compilers, you can avoid
all explicit linking by using the ``-mkl=[parallel,sequential,cluster]`` compiler flag
```
CFLAGS="-mkl=parallel"
```
more information on the flags can be found at
http://software.intel.com/en-us/articles/intel-mkl-link-line-advisor
