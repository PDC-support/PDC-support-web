

# Job arrays

Job arrays are a feature of the SLURM queue system to manage many similar jobs together. They make it easy to specify, submit and monitor a group of jobs all using the same sbatch options.

Let’s say you have the following script, which runs `myprog` with the arguments 0,1,…,9.

```bash
#!/bin/bash -l
#SBATCH  -A project
#SBATCH  -N 1
#SBATCH  -t 00:10:00

for i in $(seq 0 9); do
	srun -n 1 myprog $i
done
```

If each iteration takes a long time, you may want to run them in parallel instead.
We can achieve this by rewriting the script so that each iteration is submitted as a separate job using a job array.

```bash
#!/bin/bash -l
#SBATCH  -A project
#SBATCH  -N 1
#SBATCH  -t 00:01:00
#SBATCH  -a 0-9

srun -n 1 myprog $SLURM_ARRAY_TASK_ID
```

The option `#SBATCH -a 0-9` specifies that we want to run one job for each number between 0 and 9 inclusive. For each job the number is available in the `SLURM_ARRAY_TASK_ID` environment variable. Note that the time `-t` is reduced from 10 hours to 1 hour.

!!! note

    Submitting a large number of short jobs is bad for performance since there is an overhead associated with starting and stopping each job. Too many jobs can also slow down the whole queue system. Ideally each job should be at least 10 minutes long. For more information please see [Short jobs](short_jobs.md#short-jobs).

Once submitted, the job array is assigned an id that can be used to manipulate all jobs at once. For instance to cancel all jobs in a job array:

```bash
> sbatch job_array.sh
Submitted batch job 6975769
> scancel 6975769
```

Pending jobs in the same array are also combined into a single line in the output of `squeue`.

When using `#SBATCH --mail-type=ALL`, one email will be sent for the whole array. To get mail for each individual job use `#SBATCH --mail-type=ALL,ARRAY_TASKS`.

If the parameters of your program are not just a range of numbers you can place them in a bash array. For instance, to run `myprog apples`, `myprog pears` and `myprog oranges`:

```bash
params=(apples pears oranges)
srun -n 1 myprog ${params[$SLURM_ARRAY_TASK_ID]}
```

Read more about job arrays on the [SLURM website](https://slurm.schedmd.com/job_array.html).
