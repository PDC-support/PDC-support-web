

# Run interactively

Here’s a simplified workflow of booking a node.

![image](https://pdc-web.eecs.kth.se/files/support/images/sallocflow.PNG)

Booking a node might be suitable if you want to test and verify your code in a parallell environment, or when the code is
not time consuming but frequent adjustment is needed.

Compute nodes can be booked from the queue system for interactive use.
This means that you can run your program similar to how you run it on a local computer through terminal.

Booking an interactive node can be useful when you want to test, verify or debug your code in a parallell environment.
It’s also suitable when the program is not time consuming but is in need of frequent adjustment.
For a large scale program we recommend [Queueing jobs](queueing_jobs.md) instead,
since waiting for an interactive node booked with large amount of run time can take a lot of time.

The command to book an interactive node is salloc

```default
salloc --nodes=2 -t 1:00:00 -A <project>
```

The above command would then book two nodes for one hour.
The -A <project> should be the time allocation you are a part of.
The `-A` flag must be specified, or the command will receive an error.

```default
Job submit/allocate failed: Invalid partition or qos specification
```

You can check the time allocations you are a member of with

```default
projinfo [options]
```

Depending on how busy the supercomputer is, it might take a while before the interactive node is booked.
The terminal would then be loading while it waits in the queue. When an node is ready you will recieve a message like

```default
salloc: Granted job allocation <jobid>
```

When a node is booked, the program must be run with specific cluster commands.
Commands are detailed below for our current clusters at PDC.

On some of our cluster you can also login directly to the interactive compute node from a
separate window. After login you can run the software you like normally.
The name for the booked node be found using

```default
echo $SLURM_NODELIST
```

If you’re running a specific software, please see the [How to use module to load different softwares into your environment](../software/module.md) and [Available software](https://www.pdc.kth.se/software) .

!!! note Keep in mind that after *salloc* you’re still in the Login Node! if you execute a program without the specific commands the program will be running in the login node!

Keep in mind that the node is booked as long as you have not shut down the terminal you typed salloc, or typing the `exit` command, or the time runs out.

## Running on Dardel

Follow links to find information about [Dardel compute nodes](job_scheduling.md#dardel-compute-nodes) on Dardel and about [Dardel partitions](job_scheduling.md#dardel-partitions)

The command to book an interactive node is salloc as described above, but
the `-p` flag must be specified.

```default
salloc --nodes=2 -t 1:00:00 -A <project> -p <partition>
```

A job can be started using srun. Commands like aprun and mpirun are not available on the system.

```default
srun -n 64 ./program
```

On this cluster you can also login directly into the compute node when running
interactively, as described above. Although login to a compute node, can only
be carried out from the login node at the moment.

```default
salloc -t 10:00 -A <project> -p <partition>
echo $SLURM_NODELIST
<NODE_NAME>
ssh <NODE_NAME>
```
