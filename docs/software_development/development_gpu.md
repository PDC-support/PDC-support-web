

# Building for AMD GPUs

## The AMD ROCm development platform

The AMD Radeon Open Compute (ROCm) platform is a software stack for programming and running
of programs on GPUs. The ROCm platform has support for different programming models such as
heterogeneous interface for portability (HIP), offloading to GPU with OpenMP directives, and
the SYCL programming model.

Programs on Dardel are installed using a specific Cray Parallel Environment (CPE). The main
version of the Cray Parallel Environment on Dardel is currently 23.12 which can be loaded with

```text
ml PDC/23.12
```

To load the ROCm module version 5.7.0 and set the accelerator target to **amd-gfx90a** (AMD MI250X GPU)

```text
ml rocm/5.7.0
ml craype-accel-amd-gfx90a
```

Programs can then be built with different toolchains (Cray, Gnu, AOCC), as are available in the different
versions of the Cray Programming Environments [Compilers and libraries](development.md).

For running programs as batch jobs on the GPU nodes, see job script example 6 on [Job script examples](../run_jobs/job_scripts_dardel.md#job-script-examples).

## Compiler and linker flags environment variables

For executables that are built with the compilers of the Cray Compiler Environment (CCE),
verbose runtime information can be enabled with the environment variable `CRAY_ACC_DEBUG`
which takes values 1, 2 or 3. For the highest level of information

```text
export CRAY_ACC_DEBUG=3
```

## Build and run examples

**Example 1:** Build and run a C++ code with offloading to GPU with HIP

In this example we build and test run a Hello World C++ code in which offloading
to GPU is done with the heterogeneous interface for portability (HIP). The
program is built with the AMD hipcc compiler.

```text
# Download the source code
wget https://raw.githubusercontent.com/PDC-support/introduction-to-pdc/master/example/hello_world_gpu.cpp

# Load the ROCm module and set the accelerator target to amd gfx90a  AMD MI250X GPU 
ml rocm/5.7.0
ml craype-accel-amd-gfx90a

# We use the AMD hipcc compiler  Check the full path of the command hipcc
which hipcc
# returns
/opt/rocm-5.7.0/bin/hipcc

# Compile the code on the login node
hipcc --offload-arch=gfx90a hello_world_gpu.cpp -o hello_world_gpu.x

# Test the code in an interactive session 
# First queue to get one GPU node reserved for 10 minutes
salloc -N 1 -t 0:10:00 -A <project name> -p gpu
# wait for a node 

# then run the program
srun -n 1 ./hello_world_gpu.x

# with program output to standard out
You can access GPU devices: 0-7
GPU 0: hello world
...
```

**Example 2:** Build and run a Fortran code with offloading to GPU with OpenMP

In this example we build and test run a Fortran program that calculates the
dot product of two long vectors by means of offloading to GPU with OpenMP.
The build is done within the PrgEnv-cray environment using the Cray Compiler
Environment.

```text
# Download the source code
wget https://github.com/ENCCS/openmp-gpu/raw/main/content/exercise/ex04/solution/ex04.F90

# Load the ROCm module and set the accelerator target to amd gfx90a  AMD MI250X GPU 
ml rocm/5.7.0
ml craype-accel-amd-gfx90a

# Check which compiler the compiler wrapper is pointing to
ftn --version
# returns
Cray Fortran : Version 17.0.0

# Compile the code on the login node
ftn -fopenmp ex04.F90 -o ex04.x

# Test the code in interactive session 
# First queue to get one GPU node reserved for 10 minutes
salloc -N 1 -t 0:10:00 -A <project name> -p gpu
# wait for a node 

# then run the program
srun -n 1 ./ex04.x

# with program output to standard out
The sum is:  1.25

# Alternatively  login to the node with  for example 
ssh nid002792
# where nid002792 is one of the Dardel GPU nodes 

# Load the rocm module
ml rocm/5.7.0

# then run the program
./ex04.x

# with program output to standard out
The sum is:  1.25

# For CCE build executables  enable verbose runtime information on
# the offloading to GPU with the environment variable
export CRAY_ACC_DEBUG=3

# When rerunning the program
./ex04.x

# a detailed listing of data transfer to and from the host memory to the
# device memory is displayed
ACC: Version 5.0 of HIP already initialized, runtime version 50013601
ACC: Get Device 0
...
...
ACC: End transfer (to acc 0 bytes, to host 4 bytes)
ACC:
The sum is:  1.25
ACC: __tgt_unregister_lib
```

## References  general information

[AMD ROCm Information Portal](https://rocmdocs.amd.com/)

[ENCCS and AMD training material for ROCm](https://enccs.github.io/amd-rocm-development/)

[LUMI software development](https://docs.lumi-supercomputer.eu/development/)

[LUMI training materials](https://github.com/Lumi-supercomputer/LUMI-training-materials/)

[Frontier user guide](https://docs.olcf.ornl.gov/systems/frontier_user_guide.html)

[AMD Instinct product line](https://www.amd.com/en/graphics/instinct-server-accelerators/)

[AMD Instinct Wikipedia page](https://en.wikipedia.org/wiki/AMD_Instinct/)

[ENCCS general GPU programming course](https://enccs.github.io/gpu-programming/)

### Introductory videos from AMD

[Introduction to HIP Programming](https://www.youtube.com/watch?v=hSwgh-BXx3E)

[Introduction to AMD GPU Hardware](https://www.youtube.com/watch?v=uu-3aEyesWQ)

[GPU Programming Concepts](https://www.youtube.com/watch?v=LG9G4aA28rU)

[GPU Programming Software](https://www.youtube.com/watch?v=nkj6Z9vD-SQ)

[Porting CUDA to HIP](https://www.youtube.com/watch?v=57FwfePRd-Y)

### Heterogeneous interface for portability  HIP 

[PRACE training GPU Programming with HIP](https://events.prace-ri.eu/event/1280/attachments/1752/3402/LECTURE%20SLIDES_GPU%20programming%20with%20HIP%20%40%20CSC%20%28PTC%20%7C%20ONLINE%29%2C%209.12-10.12.2021.pdf)

[AMD’s HIP Programming Guide](https://docs.amd.com/bundle/HIP-Programming-Guide-v5.3/page/Introduction_to_HIP_Programming_Guide.html)

### OpenMP

[Michael Klemm, Intro to GPU Programming with the OpenMP API (2021-10-20)](https://www.openmp.org/wp-content/uploads/2021-10-20-Webinar-OpenMP-Offload-Programming-Introduction.pdf)

[AMD’s ROCm documentation, chapter OpenMP support](https://rocmdocs.amd.com/en/latest/Programming_Guides/openmp_support.html)

[ENCCS and CSC, OpenMP for GPU offloading](https://enccs.github.io/openmp-gpu/)

### SYCL

Codeplay’s introduction to SYCL (videos)

[Introduction to SYCL](https://www.youtube.com/watch?v=VByHaRjEQpg)

[Topology Discovery and Queue Creation](https://www.youtube.com/watch?v=s-IBxbG9Ujc)

[SYCL Kernel Functions](https://www.youtube.com/watch?v=s-IBxbG9Ujc)

[Managing Data in SYCL](https://www.youtube.com/watch?v=ft_VRuNXNHk)

[ENCCS workshop, Heterogeneous programming with SYCL](https://enccs.github.io/sycl-workshop/)

[Aksel Alpay, Universität Heidelberg, SYCL Tutorial: An Introduction to hipSYCL (video)](https://www.youtube.com/watch?v=B_DHJj-iEO8)

[hipSYCL blog, benchmarking hipSYCL with HeCBench on AMD hardware (2022-07-20)](https://hipsycl.github.io/hipsycl/amd/hecbench/hecbench-benchmarks/)
