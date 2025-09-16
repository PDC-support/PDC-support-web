CONVERGE is a revolutionary CFD software with truly autonomous meshing capabilities that eliminate the grid generation bottleneck from the simulation process. Notice that you should provide your own license to run converge on PDC clusters.
Please use command
module avail converge
to list all available versions and make sure that the correct version is loaded in the job script.
For more details, look at CONVERGE web page:
https://convergecfd.com/


# How to use


## Submitting a CONVERGE job on Dardel

**Important note: you need to set "shared_memory_flag" to 0 in your input file "inputs.in" to make it work on the new SS11 partition**

A sample script for running CONVERGE on Dardel called converge_run.sh is shown below

```
#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
#SBATCH -A <your allocation>

# The name of the script is myjob
#SBATCH -J my_job

# 10 hours wall-clock time will be given to this job
#SBATCH -t 10:00:00

# Set the partition for your job. 
#SBATCH -p <partition>

# Number of nodes
#SBATCH --nodes=2
# Number of MPI processes per node
#SBATCH --ntasks-per-node=128

#SBATCH -o output.o%J
#SBATCH -e errors.e%J


# Set the RLM license server below
#
export RLM_LICENSE=<your license server>
# Load the converge module
module load PDC
module load converge/<version>


# Run converge super
srun -n 256 converge-mpich -l super > logfile 2>&1
```


Note that this script does not include all the arguments that you can supply to CONVERGE, but you can/should add/replace whatever you want. As it is, it will work fine for your simulations if you follow the notation properly. You can submit the job using command on Tegner
sbatch converge_run.sh

