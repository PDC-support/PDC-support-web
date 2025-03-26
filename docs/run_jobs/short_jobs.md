

# Short jobs

Submitting a large number of short jobs is bad for performance since there is an overhead associated with starting and stopping each job. Too many jobs can also slow down the whole queue system. Ideally each job should be at least 10 minutes long.

Running the occasional short job is of course fine. It is often necessary for testing. The problem occurs when there is a large amount of short jobs.

There is also an overhead associated with running many short job steps. A job step is for example an invocation of `srun`. Job steps are cheaper than whole jobs, but too many of them can still cause slowdowns.

Below is some advice for how to reduce the number of short jobs. If you need help with this please [Contact Support](../contact/contact_support.md#contact-support).

If you are submitting many similar jobs, also consider using [Job arrays](job_arrays.md#job-arrays).

## Pack short jobs together

Several short jobs may be packed together into a single larger job where they run serially to increase the length of the job and reduce the number of jobs.

Let’s say you have the following job script:

```bash
#!/bin/bash -l
#SBATCH  -A project
#SBATCH  -N 1
#SBATCH  -t 00:01:00

srun -n 1 myprog $1
```

The jobs are submitted with the following command, where `x` is the data for the job:

```bash
sbatch short_job.sh x
```

By increasing the time limit and supplying multiple data we can run the program more times in the same job. The following script will run `myprog` once for each of the arguments to `sbatch`.

```bash
#!/bin/bash -l
#SBATCH  -A project
#SBATCH  -N 1
#SBATCH  -t 00:10:00

for arg in "$@"; do
	srun -n 1 myprog $arg
done
```

The special symbol `"$@"` means all arguments to the script. The jobs are now submitted using:

```bash
sbatch packed_job.sh x0 x1 x2 x3 x4 x5 x6 x7 x8 x9
```

## Use fewer cores

Reducing the level of parallelism will make the jobs take longer, while allowing more of them to run at the same time. An added benefit is that this often increases efficiency as there is less communication.

If your job runs on multiple nodes, then it is usually simple to just decrease the number of nodes used.

If you job runs on one node, then it is usually possible to run multiple instances of the program at the same time, each using a fewer number of cores. Let’s say you have the following OpenMP job.

```bash
#!/bin/bash -l
#SBATCH -A project
#SBATCH -N 1
#SBATCH -t 00:01:00

export OMP_NUM_THREADS=32

srun myprog $1
```

Using an approach similar to [Pack short jobs together](), we can pack multiple jobs into one. This time the packed jobs can run in parallel on different cores. Reducing the number of threads from 32 to 4 means that we can run 32/4=8 instances of the program at the same time. The script below starts a job step running another script called `inner.sh`.

```bash
#!/bin/bash -l
#SBATCH -A project
#SBATCH -N 1
#SBATCH -t 00:08:00

export OMP_NUM_THREADS=4

srun ./inner.sh "$@"
```

The inner script shown below starts starts several parallel instances of `myprog`. The `&` is used to not wait for one command to finish before running the next one, and `wait` is used to ensure that all instances are done before exiting.

```bash
#!/bin/bash

for arg in "$@"; do
	myprog $arg &
done

wait
```
