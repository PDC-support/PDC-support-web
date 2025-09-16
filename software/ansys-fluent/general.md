Ansys/Fluent is a computational fluid dynamics (CFD) software. Fluent is a general-purpose CFD code based on the finite volume method on a collocated grid.   As of 2012 KTH have made a joint purchase of ANSYS (in which Fluent is one component).

# How to use Ansys/Fluent on PDC machines
In order to use ANSYS Fluent at PDC you need to:

1. Have an account at PDC
2. Check with the Ansys license owner at your department to allow running Ansys/Fluent at PDC
3. Contact KTH if you have problems/questions with Ansys/Fluent licenses.

Use the  commands
```
module avail fluent
```
to list all available versions and make sure that the correct version is loaded in the job script. If the version using which the .cas file was created can't be found in the list of installed versions, please contact PDC (support@pdc.kth.se).

To load a specific version of the fluent module, the following command can be used

```
module load fluent/<version>
```
where `<version>` is replaced by the actual version, as displayed when using the module avail command. 

For more details, look at Ansys web page:
[http://www.ansys.com/](http://www.ansys.com/)


# How to use


## Submitting a Fluent job on Dardel
Before preparing your script, you need to make a journal file to give tasks to Fluent. It should be in the same directory as your job subbmission script. A sample journal file can be found below
```
; -----------------------------------------------------------
;SAMPLE JOURNAL FILE

;read case file (*.cas) that had previously been prepared file/read-case fluent.cas

;read data file (*.dat) in case you are starting simulation from a saved file
;comment it if you start from zero
file/read-data mycase.dat

;run 10 iterations
solve/iterate 10

;write data
file/write-data results.dat

;exit fluent
exit yes
; ------------------------------------------------------------
```
Then you can use the following script for running Ansys/Fluent on Dardel:
```
#!/bin/bash 

# Name of your job
#SBATCH -J test

#SBATCH -A <allocation>

# Wall-clock time will be given to this job
#SBATCH -t 10:00:00

# Number of nodes
#SBATCH -N 1

# Set the partition for your job. 
#SBATCH -p <partition>

#SBATCH -e error_file.e%J

# load module fluent v24.2
# module load PDC
module load fluent/24.2

# The Journal file
JOURNALFILE=journalfile.jou

# Set the license server below
export ANSYSLMD_LICENSE_FILE=<license file>
export ANSYSLI_SERVERS=<license server>
# If you are KTH user, contact PDC support or KTH IT for license server information

# Total number of Processors
# NPROCS=1x128 = number of nodes x number of processors per node
NPROCS=128

fluent 3ddp -g -t $NPROCS -mpi=cray -i $JOURNALFILE > my_output_file.$SLURM_JOBID

```

Then you can submit your job using *sbatch*
```
sbatch <job_script>.sh
```
