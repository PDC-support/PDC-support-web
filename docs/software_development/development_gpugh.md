

# Building for NVIDIA GPUs

## The Cray Parallel Environment

Programs on Dardel are installed using a specific Cray Parallel Environment (CPE). On Dardel's Grace Hopper nodes, the default
version of the Cray Parallel Environment is currently 25.03. To make available applications that have been built under CPE/25.03, load the PDC/25.03 module

```text
ml PDC/25.03
```

## The NVIDIA CUDA ToolKit and the NVIDIA HPC SDK

The NVIDIA CUDA ToolKit provides a development and runtime environment for GPU accelerated applications. The NVIDIA HPC Software Development Kit (SDK) extends the CUDA ToolKit with libraries and tools for developing, building and running GPU accelerated software on NVIDIA GPUs in the context of high performance computing (HPC) applications.

## The cpeNVIDIA programming environment

In analogue with the programming environments for AMD CPUs and AMD GPUs, dedicated programming environments are available for the NVIDIA Grace Hopper nodes. On Dardel the main programming environment for building and running on NVIDIA is **cpeNVIDIA** which can be loaded with

```text
ml cpeNVIDIA
```

This will set the host parallel environment to **craype-arm-grace** (Arm Grace) and the accelerator target to **craype-accel-nvidia90** (NVIDIA Hopper). **craype-arm-grace** adds references to libraries for the purpose of building for Arm Grace architecture whereas **craype-accel-nvidia90** supports the NVIDIA H100 Tensor Core GPU based on the new NVIDIA Hopper GPU architecture. Loading the **cpeNVIDIA** environment also activates additional modules, which can be listed with

```text
ml show cpeNVIDIA
```

The **cpeNVIDIA** toolchain is suitable for programs that require the NVIDIA Fortran compiler in order to build Fortran code with OpenACC offloading to GPU, or code using CUDA Fortran.

## Combining different compilers

In general, applications can be built using multiple compilers for the different sets of source code files, e.g. using one compiler for the code for the host, and another compiler for the code for the device. A build environment of this kind can be set up by first loading the programming environment of choice for the host, followed by loading the Cuda Toolkit. One combination that is of high relevance is to make use of the compilers in the Gnu compiler collection for C, C++, and Fortran code, and the NVIDIA nvcc compiler for the CUDA code. Such an environment can be set up with for instance

```text
ml PrgEnv-gnu
ml gcc-native/13.2
ml cudatoolkit/24.11_12.6
ml cray-fftw/3.3.10.10
ml cmake/4.1.2
```

where also a module for FFT on the host and a recent CMake build system is loaded.

## References

[NVIDIA CUDA ToolKit](https://developer.nvidia.com/cuda-toolkit)

[NVIDIA HPC SDK](https://developer.nvidia.com/hpc-sdk)

[NVIDIA Nsight Developer Tools](https://developer.nvidia.com/tools-overview)