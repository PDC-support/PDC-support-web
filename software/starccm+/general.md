## How to use
# How to use StarCCM+ on PDC machines
StarCCM+ is commercial software, and PDC does not have a license. All licenses to use StarCCM+ at PDC must be supplied by the users.

The Star-CCM files can be accessed by loading the appropriate modules. To see which versions of Star-CCM+ are available use the command 
```
module avail starccm+
```
In order to use StarCCM+ at PDC you must provide your own license for the software. You can either use the environment variable
`CDLMD_LICENSE_FILE` to set to point to the correct license server (not the PoD server 1999@flex.cd-adapco.com), or get access to STAR-CCM+ through license keys generated "power-on-demand" with additional options in the command line
```
-podkey your_license_key -licpath 1999@flex.cd-adapco.com
```
where "your_license_key" is the license key.

# Running on the Batch system
sample job script
```
#!/bin/bash -l

#SBATCH -A <allocation>
#SBATCH -J starccm
#SBATCH -t 01:00:00
#SBATCH --nodes=2
#SBATCH -p main
#SBATCH --ntasks-per-node=128
#SBATCH -e error_file.e%J
#SBATCH -o output_file.o%J

# module load PDC
module load starccm+/<version>

sim_file="my_case.sim"
export TMPDIR=$(pwd)/starccm_tmp/
LUSTRE_ROOT=$(pwd)/starccm_tmp/StarCCM_config
mpi=crayex

# If you use a license server
export CDLMD_LICENSE_FILE=<license-server>

starccm+ -power -mpidriver $mpi -np 256 -arch linux-x86_64-2.28 -batch run  -pio -nbuserdir $LUSTRE_ROOT  ${sim_file}> my_output_file 2>&1

# If you use POD key, just add the following to the starccm+ command:
# -podkey <your key> -licpath 1999@flex.cd-adapco.com
```


You can control number of MPI processes by `-np` option in the execution command
```
-np 256
```
