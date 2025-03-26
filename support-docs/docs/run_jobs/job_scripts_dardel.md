

# Job script examples

Follow links to find information about [Dardel compute nodes](job_scheduling.md#dardel-compute-nodes) on Dardel and about [Dardel partitions](job_scheduling.md#dardel-partitions)

!!! note 
    It is advisable to use parameter flags in the **#SBATCH** tags rather than as parameters in **srun**,
    to increase clarity of your scripts.

**Example 1:**

Below is a job script example for a pure MPI job. For PDC-installed programs, you can find examples in the [software page](https://support.pdc.kth.se/doc/applications/).

```text
#! bin bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A naissYYYY X XX

# The name of the script is myjob
#SBATCH -J myjob

# The partition
#SBATCH -p main

# 10 hours wall clock time will be given to this job
#SBATCH -t 10:00:00

# Number of nodes
#SBATCH --nodes=4

# Number of MPI processes per node
#SBATCH --ntasks-per-node=128

# Run the executable named myexe
# and write the output into my output file
srun ./myexe > my_output_file
```

**Example 2:**

Below is another example for a hybrid MPI+OpenMP program. This example will place 16 MPI processes with 8 threads each on each compute node. The *--hint=nomultithread* option for *srun* is to ensure correct placement of OpenMP threads.

```text
#! bin bash  l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A naissYYYY X XX

# The name of the script is myjob
#SBATCH -J myjob

# The partition
#SBATCH -p main

# 10 hours wall clock time will be given to this job
#SBATCH -t 10:00:00

# Number of Nodes
#SBATCH --nodes=4

# Number of MPI tasks per node
#SBATCH --ntasks-per-node=16
# Number of logical cores hosting OpenMP threads
# Note that cpus per task is set as 2x OMP NUM THREADS
#SBATCH --cpus-per-task=8

# Number and placement of OpenMP threads
export OMP_NUM_THREADS=8
export OMP_PLACES=cores

# for slurm 22 05
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

# Run the executable named myexe
# and write the output into my output file
srun --hint=nomultithread ./myexe > my_output_file
```

**Example 3:**

Below is an example of a *job array*, in which 100 separate jobs are
executed in one shot in the corresponding directories.
Job arrays are useful to manage large numbers of jobs which run on the
same number of nodes and take roughly the same time to complete.
For more information see [Job arrays](job_arrays.md#job-arrays).

```text
#! bin bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A naissYYYY X XX

# The name of the script is myjob
#SBATCH -J myjobarray

# The partition
#SBATCH -p main

# 10 hours wall clock time will be given to this job
#SBATCH -t 10:00:00

# Number of nodes used for each individual job
#SBATCH --nodes=1

# Number of MPI tasks per node
#SBATCH --ntasks-per-node=128

# Indices of individual jobs in the job array
#SBATCH  a 0 99

# Fetch one directory from the array based on the task ID
# Note  index starts from 0
CURRENT_DIR=data${SLURM_ARRAY_TASK_ID}
echo "Running simulation in $CURRENT_DIR"

# Go to job folder
cd $CURRENT_DIR
echo "Simulation in $CURRENT_DIR" > result

# Run individual job
srun ./myexe > my_output_file
```

**Example 4:**

Below are a job script example for MPI executed on a shared node using 10 cores.
Please note that the `shared` partition is used, since this job cannot saturate
a single node on Dardel.

```text
#! bin bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A naissYYYY X XX

# The name of the script is myjob
#SBATCH -J myjob

# The partition
#SBATCH -p shared

# The number of tasks requested
#SBATCH -n 10

# The number of tasks for each node requested
#SBATCH --ntasks-per-node 2

# 10 hours wall clock time will be given to this job
#SBATCH -t 10:00:00

# Run the executable named myexe
# and write the output into my output file
srun -n 20 ./myexe > my_output_file
```

**Example 5:**

Below are a job script example for an OpenMP job executed on a shared node using 16 cores.
Please note that the `shared` partition is used, since this job cannot saturate
a single node on Dardel.

```text
#! bin bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A naissYYYY X XX

# The name of the script is myjob
#SBATCH -J myjob

# The partition
#SBATCH -p shared

# Number of tasks
#SBATCH -n 1

# Number of cpus per task
#SBATCH -c 16

# 10 hours wall clock time will be given to this job
#SBATCH -t 10:00:00

export OMP_NUM_THREADS=8

# Run the executable named myexe
# and write the output into my output file
srun ./myexe > my_output_file
```

In case you are running more than the granted number of cores on the shared node, a similar
error will occur

```default
srun: error: Unable to create step for job <JOBID>: More processors requested than permitted
```

!!! note
    The amount of RAM you are getting on shared nodes is directly proportional to the number of processors you are asking for.
    For example, if you are asking for half of the processors on one node, you will also get a max of half the amount of RAM on that node.

**Example 6:**

Below is a job script example for a job running on a Dardel GPU node.

```text
#! bin bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A naissYYYY X XX

# The name of the script is myjob
#SBATCH -J myjob

# The partition
#SBATCH -p gpu

# 1 hour wall clock time will be given to this job
#SBATCH -t 01:00:00

# Number of nodes
#SBATCH --nodes=1

# Number of MPI processes per node
#SBATCH --ntasks per node=1

# Load a ROCm module and set the accelerator target
ml rocm/5.0.2
ml craype-accel-amd-gfx90a

# Run the executable named myexe
# and write the output into my output file
srun ./myexe > my_output_file
```
