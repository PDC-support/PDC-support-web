
# Data Management

This section gives you information about PDC’s storage solutions.
Working with PDC can involve transferring data back and forth between your local machine and PDC resources, or between different systems at PDC.

If you have NAISS Swestore allocation, please check [How to use Swestore](file_transfer_swestore-dcache.md) section on how to transfer files to/from Swestore.

## Where to store my data

As the speed of CPU computations keep increasing, the relatively slow rate of input/output (I/O) or
data accessing operations can create bottlenecks and cause programs to slow down significantly.
Therefore it is very important to pay attention to how your programs are doing I/O and accessing data
as that can have a huge impact on the run time of your jobs. Here, you will find a quick guide to storing data,
ideal if you have just started to use PDC resources.

## Nodes for file operations

At PDC we have a number of transfer nodes setup.
These nodes are dedicated for large file transfers but also
for extensive file operations involving large amount of data
or many files. It is important that you use these nodes for extensive
file operations as not to overload the login node.

**Dedicated transfer nodes for large file transfers will be set up on Dardel. In the meanwhile,
please use the dardel.pdc.kth.se login node for the file transfers.**

| Name              | Type                | Usage                                             |
|-------------------|---------------------|---------------------------------------------------|
| dardel.pdc.kth.se | Login node (Dardel) | Submitting jobs and small file transfers          |
| dardel.pdc.kth.se | Login node (Dardel) | Large transfers and operations on the file system |

## PDC environmental variables

To simplify for the user how to find different folders, PDC has provided a number of specific variables
which indicate in which folders data should be stored.
These variables are loaded by default

Table of the environmental variables

| Name         | Function                                  | Location on Dardel                   |
|--------------|-------------------------------------------|--------------------------------------|
| PDC_BACKUP   | Where important data are backed up.       | Your klemming home directory         |
| PDC_RESOURCE | Name of the cluster you are logged into   | Dardel                               |
| PDC_SITE     | Name of the site                          | PDC                                  |
| PDC_TMP      | Scratch folder for storing temporary data | /cfs/klemming/scratch/[U]/[USERNAME] |
| PDC_SHUB     | Singularity containers folder             | /pdc/software/resources/sing_hub     |
