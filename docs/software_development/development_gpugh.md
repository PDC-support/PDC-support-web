

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

In analogue with the programming environments for AMD CPUs and AMD GPUs, dedicated programming environments are available for the NVIDIA Grace Hopper nodes. On Dardel the main programming environment for building and running on NVIDIA is cpeNVIDIA which can be loaded with

```text
ml cpeNVIDIA
```

This will set the host parallel environment to **craype-arm-grace** (Arm Grace) and the accelerator target to **craype-accel-nvidia90** (NVIDIA Hopper). **craype-arm-grace** adds references to libraries for the purpose of building for Arm Grace architecture whereas **craype-accel-nvidia90** supports the NVIDIA H100 Tensor Core GPU based on the new NVIDIA Hopper GPU architecture.

## References

[NVIDIA CUDA ToolKit](https://developer.nvidia.com/cuda-toolkit)

[NVIDIA HPC SDK](https://developer.nvidia.com/hpc-sdk)

[NVIDIA Nsight Developer Tools](https://developer.nvidia.com/tools-overview)