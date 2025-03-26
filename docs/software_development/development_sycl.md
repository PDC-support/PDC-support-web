**Example 3:** Build and run a C++ code with offloading to GPU with SYCL

In this example we build and test run a SYCL C++ program that performs
**axpy** arithmetic operations. The build is done within the PrgEnv-gnu environment
using the **syclcc** compiler and the CMake build system.

```text
# Download the source code and its accompanying CMakeLists txt
wget https://raw.githubusercontent.com/ENCCS/sycl-workshop/main/content/code/day-1/06_axpy-usm/solution/axpy.cpp
wget https://raw.githubusercontent.com/ENCCS/sycl-workshop/main/content/code/day-1/06_axpy-usm/solution/CMakeLists.txt

# Load the AdaptiveCpp module and set the accelerator target to amd gfx90a  AMD MI250X GPU 
ml craype-accel-amd-gfx90a
ml PDC/23.03
ml adaptivecpp/23.10.0-cpeGNU-23.03-rocm-5.3.3-llvm
ml cmake/3.27.7

# We use the syclcc compiler together with CMake  Check the full path of the command syclcc
which syclcc
# returns
/pdc/software/23.03/eb/software/adaptivecpp/23.10.0-cpeGNU-23.03-rocm-5.3.3-llvm/bin/syclcc

# Configure and compile the code with Cmake
mkdir build
cd build
cmake ..
make

**Note:** If needed, replace in ``CMakeLists.txt`` the line ``find_package(hipSYCL CONFIG REQUIRED)``
with the line ``find_package(AdaptiveCpp CONFIG REQUIRED)``.

# Test the code in interactive session 
# First queue to get one GPU node reserved for 10 minutes
salloc -N 1 -t 0:10:00 -A <project name> -p gpu
# wait for a node  Then login to the node with  for example 
ssh nid002860
# where nid002860 is one of the Dardel GPU nodes 

# Load the PDC and hipsycl modules
ml PDC/23.03
ml adaptivecpp/23.10.0-cpeGNU-23.03-rocm-5.3.3-llvm

# then run the program
./axpy

# with program output to standard out
Running on:
Checking results...
Nice job!
```
