

# Job scripts

To submit a job to the queue system some details have to be specified,
for instance the compute project and the number of nodes required.
In a job script, this is done by adding lines starting with `#SBATCH`.
These options are then passed to the SLURM, the queue system.
They are not the same as options to the `srun` command, and both needed to be configured properly.

The following list explains the most common options specified in job scripts. For a complete reference please consult the output of `man sbatch`.

!!! note

    All `#SBATCH` options must be at the top of the script file.


`#SBATCH -A <project>`
: The compute project the job is part of. Is used to prioritize jobs.
  The `-A` flag must be specified, or the submission will fail:
  <br/>
  ```default
  Job submit/allocate failed: Invalid partition or qos specification
  ```
  <br/>
  You can check the time allocations you are a member of by running the command:
  <br/>
  ```default
  projinfo
  ```


`#SBATCH -t <hh:mm:ss>`
: Maximum job run time. Allows SLURM to schedule jobs more effectively. A job with shorter run time will start quicker than a long running job. Other possible formats are <minutes>, <days-hours>, <days-hours:minutes>.


`#SBATCH -N <nodes>`
: Number of nodes to reserve.


`#SBATCH -n <tasks>`
: Number of tasks that the job will use. Also known as processes or MPI ranks.


`#SBATCH --ntasks-per-node=<tasks per node>`
: Set the number of tasks per node. Useful with MPI/OpenMP hybrids where `--ntasks-per-node=1` can be used.


`#SBATCH --gres=gpu:X`
:


`#SBATCH -J <jobname>`
: Name shown in the queue. The default is the name of the job script.


`#SBATCH -e <file>`
: File where error messages are written (stderr). Can include special symbols starting with a percent sign. The job id %j can be used to distinguish different runs. The default is `slurm-%j.out`.


`#SBATCH -o <file>`
: File where output messages are written (stdout). Same format as the error file above. The default is `slurm-%j.out`.


`#SBATCH -a 0-N`
: Run job array with a total of N+1 jobs. Job arrays are a convienient way to start many similar jobs. Each job gets a different value in the environment variable `SLURM_ARRAY_TASK_ID`. For a more detailed explanation see [Job arrays](job_arrays.md#job-arrays).


`#SBATCH --mail-type=ALL`
: Request an email when the job starts and ends.


`#SBATCH -p <partition name>`
: Specify the partition where the job should run. The partition can be a comma-separated list if the job can run on more than one partition.


`#SBATCH -C <feature>`
: Specify additional constraints on the requested nodes. To list the available features of all the nodes, run:
  <br/>
  ```default
  sinfo -o %f
  ```

You can test if the syntax of a job script is correct by running:

```default
sbatch --test-only my_script.sh
```

This will check the parameters and print an estimation of when the job would be started, without adding it to the queue.

For examples of job scripts please see the following pages:

* [Job script examples](job_scripts_dardel.md)
* [Job arrays](job_arrays.md)
* [Short jobs](short_jobs.md)
  * [Pack short jobs together](short_jobs.md#pack-short-jobs-together)
  * [Use fewer cores](short_jobs.md#use-fewer-cores)
