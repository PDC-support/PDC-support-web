
# How to use OpenFOAM on PDC machines
OpenFOAM is a free, open source CFD software package.

See also [http://www.openfoam.com](http://www.openfoam.com) and [http://www.openfoam.org](http://www.openfoam.org)

To see which versions of OpenFOAM are installed on any of the machines at PDC log into the machine and type
`module avail openfoam`
As the current versions of OpenFOAM are very easily to generate massive small files,  you mast consider questions before running OpenFOAM such as:

- **How often do you save your solution?**
- **What trace/history of your iterations do you write to file(s)?**

To control this behavior you need to modify the corresponding parameters in
**system/controlDict**
```
writeControl    timeStep;
writeInterval   10000;
```
i.e. specify the number of timeStep for *writeInterval* as large as possible.

Moreover, setting **writeCompression** to compressed would really do a damper on the **/cfs/klemming** file system. We already know that if someone set **runTimeModifiable** to **yes**  that will have an adverse effect on performance  since OpenFOAM then will check a lot of files at every single iteration. As a result, you should adapt the simulations to the system by tweaking the following parameters:
```
writeCompression                    uncompressed;
runTimeModifiable                   no;
```
**It is highly recommended that you run OpenFoam on your project directory to avoid any disk quota problems**

See [https://www.pdc.kth.se/support/documents/data_management/lustre.html](https://www.pdc.kth.se/support/documents/data_management/lustre.html) for more information about the project directory


## How to use


# Running on the Batch system
sample job script

```
#!/bin/bash -l

#The name of the script is mytest
#SBATCH -J mytest

#SBATCH -A <allocation>

# 12 hour wall-clock time will be given to this job
#SBATCH -t 12:00:00

# Set the partition for your job. 
#SBATCH -p <partition>

# Number of nodes
#SBATCH --nodes=2

# Number of MPI processes per node (default 128)
#SBATCH --ntasks-per-node=128

# Load the openfoam module
module load PDC
module load openfoam/v2406

# Set the openfoam environment variables
. $FOAM_BASHRC

# Change OpenFoam user directory to the project directory
# Comment the three lines below if not running on the project directory

WM_PROJECT_DIRECTORY2=$(pwd)
export WM_PROJECT_USER_DIR=$WM_PROJECT_DIRECTORY2/$WM_PROJECT/$USER-$WM_PROJECT_VERSION
export FOAM_RUN=WM_PROJECT_USER_DIR/run

# Start the OpenFOAM job with 256 MPI-tasks on 2 nodes

srun -n 256 -N 2 <openfoam binary> -case <path to case directory> -parallel > my_output_file 2>&1
```
