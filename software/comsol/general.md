
# How to use Comsol on PDC machines
KTH has a site license for Comsol Multiphysics and almost all the modules that students and employees at KTH can use for academic work. PDC users outside KTH cannot use Comsol unless they supply their own license - to run a cluster simulation you need to own a floating network license.
To see which versions of comsol are installed on any of the machines at PDC log into the machine and type
module avail comsol
You should always run comsol simulations on */cfs/klemming* file system.
Notice also that the log and temporary files are stored in $HOME/.comsol by default. In order to avoid fully disk qutoa in the home directory  (can be checked using command *fs lq ~*),  you can do in the first time likes 
```
$ rm -rf ~/.comsol  # remove the directory .comsol
$ mkdir /cfs/klemming/scratch/<u>/<username>/.comsol # replace <u>/<username> with yours
$ ln -s /cfs/klemming/scratch/<u>/<username>/.comsol ~/.comsol # replace <u>/<username> with yours
```
i.e. soft link the $HOME/.comsol to a directory on /cfs/klemming system.
You can also redirect the temporary directory to /cfs/klemming system using comsol flags *-tmpdir* and *-recoverdir* in the job script likes 
```
$ rm -rf ~/.comsol/*
$ comsol ... -tmpdir /cfs/klemming/scratch/<u>/<user>/tmp -recoverydir /cfs/klemming/scratch/<u>/<username>/rec
```
where *...* represents the other comsol flags.
More details see
http://www.comsol.com


## How to use

```
module load comsol
```



# Running Comsol on Dardel
To submit a job on single node (containing 128 cores), you can do so by creating a simple script (comsol_run.sh) which includes:
```
#!/bin/bash
# The -l above is required to get the full environment with modules 

# Set job name
#SBATCH -J my_job

# 10 hours wall-clock time will be given to this job
#SBATCH -t 10:00:00

# Set the partition for your job. 
#SBATCH -p <partition>

# set the project to be charged for this
#SBATCH -A <your allocation>

# Number of nodes(every node has 128 cores)
#SBATCH --nodes=1

#SBATCH -e error_file.e%J
#SBATCH -o output_file.o%J

# load comsol module
# module load PDC
module add comsol/5.6


export LM_LICENSE_FILE=<your license server>

work_dir=$(pwd)/temp
pref_dir=$work_dir/prefs
conf_dir=$pref_dir/configuration
data_dir=$pref_dir/data
rec_dir=$work_dir/recovery
tmp_dir=$work_dir/tmp


mkdir -p $pref_dir
mkdir -p $rec_dir
mkdir -p $tmp_dir
mkdir -p $conf_dir


comsol batch -np 32 -prefsdir $pref_dir -configuration ${conf_dir}/conf.${SLURM_JOBID} -data ${data_dir}/data.${SLURM_JOBID} -recoverydir ${rec_dir} -tmpdir ${tmp_dir} -inputfile  input.mph -outputfile output.mph -batchlog my_output_file.${SLURM_JOBID}

```

and submit the script on the login node:
```
sbatch comsol_run.sh
```
You can control number of cores by *-np* option.

**It is recommended to clear temp directory after your simulations since it can cause your storage go above quota and you lose write permissions**

