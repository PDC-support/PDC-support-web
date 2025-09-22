
# How to Run Jobs

Many researchers run their program on PDC’s computer systems, often simultaneously. For this, the computer systems need workload management and job scheduling. For job scheduling PDC uses [Slurm Workload Manager](https://slurm.schedmd.com/) .

When you login to the supercomputer with ssh, you login to a designated **login node** in your *Klemming home directory*. Here you can modify your scripts and manage your files.

![image](https://pdc-web.eecs.kth.se/files/support/images/LoginNodeWarning.PNG)

To run your script/program on the computer nodes, you either write a [job script](job_scripts.md) describing what resources you need and submit this using the `sbatch` command as described [here](queueing_jobs.md), or run the script/program interactively as described [here](run_interactively.md).

## How jobs are scheduled

The queue system uses two main methods to decide which jobs are run. These are called *fair-share* and *backfill*. Unlike some other centers, the time a job has been in the queue is not a factor.

### Fair share

The goal of the fair share algorithm is to make sure that all projects can
use their fair share of the available resources within a reasonable time
frame. The priority that a job (belonging to a particular project) is given
will depend on how much of that project’s time quota has been used recently
in relation to the quotas of jobs belonging to other projects - the effect of
this on the priority declines gradually with a half-life of 14 days. So jobs
submitted by projects that have not used much of their quota recently will be
given high priority, and vice versa.

### Backfill

As well as having a main queue to ensure that the systems are as full as possible, the job scheduling system also implements “backfill”. If the next job in the queue is large (i.e., it requires a significant number of nodes to run), the scheduler accumulates nodes as they become available until there are enough to start running the large job. Backfill means that the scheduler looks for smaller jobs that could start on nodes that are free now, and which would finish before there are enough nodes free for the large job to start. For backfill to work well, the scheduler needs to know how long jobs will take. So, to take advantage of the possibility of backfill, you should set the maximum time your job needs to run as accurately as possible in your submit scripts.

This graph shows the percentage of the nodes on Beskow (previous PDC’s supercomputer)
that were in use on different dates from early 2015 till late 2016. You can see how
the scheduler makes good use of Beskow as nearly all of the available nodes are being used
all the time.

!!! note

    All researchers sharing a particular time allocation have the same priority. This means that if other people in your time project have used up lots of the allocated time recently, then any jobs you (or they) submit within
    that project will be given the same low priority.

### Example of scheduling

Consider a couple of researchers, Anna and Björn with projects A and
B. Of course both Anna and Björn would like their jobs to be run as
soon as possible.

Assume now that project B has used less of its time allocation than
project A. In this case, the scheduler will give priority to Björn’s
job.

Even if Anna has not used any time herself, this does not make any
difference as it is the total amount of time recently used by each
project that is taken into consideration when deciding which job will
be scheduled next.

## Dardel compute nodes

Compute nodes on Dardel have five different flavors with different amounts of memory. A certain amount of the memory is reserved for the operating system and system software. Therefore the amount of memory available for user software is also listed in the table below. All nodes have the same dual socket processors, for a total of 256 logical cores (128 physical cores w. two hyperthreads each) per node.

| Node type   |   Node count | RAM    | Partition          | Available   | Example used flag   |
|-------------|--------------|--------|--------------------|-------------|---------------------|
| Thin node   |          700 | 256 GB | main, shared, long | 227328 MB   |                     |
| Large node  |          268 | 512 GB | main, memory       | 456704 MB   | `--mem=440GB`       |
| Huge node   |            8 | 1 TB   | main, memory       | 915456 MB   | `--mem=880GB`       |
| Giant node  |           10 | 2 TB   | memory             | 1832960 MB  | `--mem=1760GB`      |
| GPU node    |           62 | 512 GB | gpu                | 456704 MB   | `--mem=440GB`       |

More details on the hardware is available at
[https://www.pdc.kth.se/hpc-services/computing-systems/about-dardel-1.1053338](https://www.pdc.kth.se/hpc-services/computing-systems/about-dardel-1.1053338).

Different node types are allocated based on the SLURM partition (`-p`) and the `--mem` or `--mem-per-cpu` flags. By default, any free node in the partition can be allocated to the job. Using the `--mem=X` flag restricts the set of eligible nodes to those with at least X amount of available memory.

The following configuration allocates one node with at least 250 GB of available memory in the main partition, i.e. a large or huge node:

```default
#SBATCH --mem=250GB
#SBATCH -p main
```

The `--mem` flag imposes a hard upper limit on the amount of memory the job can use.
In the above example, even if the job is allocated a node with 1 TB of memory, it will not be able to use more than 250 GB of memory due to this limitation.



## Dardel partitions

The compute nodes on Dardel are divided into five partitions. Each job must specify one of these partitions using the `-p` flag. The table below explains the difference between the partitions. See the table above for descriptions of the various node types.

| Partition name   | Characteristics                                                                                                                                                                                     |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| main             | Thin, large and huge nodes<br/><br/>Job gets whole nodes (exclusive)<br/><br/>Maximum job time 24 hours                                                                                             |
| long             | Thin nodes<br/><br/>Job gets whole nodes (exclusive)<br/><br/>Maximum job time 7 days                                                                                                               |
| shared           | Thin nodes<br/><br/>Jobs are allocated to cores, not nodes<br/><br/>By default granted one core, get more with `-n or -c`<br/><br/>Job shares node with other jobs<br/><br/>Maximum job time 7 days |
| memory           | Large, huge and giant nodes<br/><br/>Job gets whole nodes (exclusive)<br/><br/>Maximum job time 7 days                                                                                              |
| gpu              | GPU nodes<br/><br/>Job gets whole nodes (exclusive)<br/><br/>Maximum job time 24 hours                                                                                                              |

## How to run on shared partitions

Running on the shared partition is a little bit different than running on exclusive nodes.
First you need to specify the number of cores you will be using, and, at the same time, you get
an equivalent size of RAM for your job.

### Defining the number of cores or memory

When running on shared nodes, you need to add the number of cores you will be using or the amount of memory you need.
The amount of memory is equivalent to the amount of cores you are asking for and viceversa.
For example, we are using a node with 256 logical cores (128 physical cores) and 256 Gbytes of RAM.
If you are asking for 20 cores, you will receive 17 Gbytes of RAM. Instead of you are asking for 80 Gbytes of RAM, you will automatically receive 94 cores.
The cores or memory that is the largest for the job will dictate what is needed.

### Paremeters needed on shared nodes

| Parameter | Description |
| --- | --- |
| `-n [tasks]` | Allocates ntasks |
| `--cpus-per-task=[cores]` | Allocates logical [cores]=ntasks*cpu-per-task. (Default: cpus-per-task=1) |
| `--mem=[RAM in Mbytes]` | The max amount of RAM allocated for your job |

**Example 1:** On a shared node with 128 physical cores, 256 Gbytes RAM.
In this case you will receive 20 logical cores, 17 GBytes RAM
```default
#SBATCH  -p shared
#SBATCH  --ntasks=10
#SBATCH --cpus-per-task=2
```

**Example 2:** On a shared node with 128 physical cores, 256 Gbytes RAM.
In this case you will receive 48 logical cores, 40 GBytes RAM. The amount of cores you ask for does not cover your need for RAM.
```default
#SBATCH  -p shared
#SBATCH  --ntasks=2
#SBATCH --mem=40G
```
