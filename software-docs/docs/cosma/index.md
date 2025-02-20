---
title: Information about cosma
keywords:
  - Libraries
---
# Cosma

## Installed versions

| Resource | Version |
|---|---|
| Dardel/cpe23.12 | 2.6.6 |
| Dardel/cpe23.03 | 2.6.6 |
| Dardel-GPU/cpe23.03.gpu | 2.6.6 |
| Dardel-GPU/cpe23.12.gpu | 2.6.6 |

## General information

COSMA is a parallel, high-performance, GPU-accelerated, matrix-matrix multiplication algorithm that is communication-optimal for all combinations of matrix dimensions, number of processors and memory sizes, without the need for any parameter tuning. For more information see the [COSMA homepage](https://github.com/eth-cscs/COSMA).

## How to use

You can check available COSMA modules using
```
ml spider cosma
```

For example, load the module for the COSMA library 2.6.6 with GPU backend
```
ml PDC/<version>
ml cosma/2.6.6-cpeGNU-23.12-gpu
```

To see what environment variables are set when loading the module
```
ml show cosma/2.6.6-cpeGNU-23.12-gpu
```

