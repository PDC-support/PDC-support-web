Multiple versions of Python are installed on PDC machines.
To see which version of Python is available by default use the command:
```
python -V
```

!!! Attention

    The Anaconda3 module will be decommissioned by 2024-12-31, due to license policy changes in the Anaconda organization. Please migrate to use the module miniconda3 instead.

# Miniconda
Python has a very large number of optional packages for
large-scale data processing and scientific computing
which are not available in the default system python.

To list available Miniconda modules, type:
```
$ ml PDC/<version>
$ ml av miniconda3
```

For example, to load Miniconda version 2024.07.1 type:
```
$ ml miniconda3/24.7.1-0-cpeGNU-23.12
```

After loading a miniconda module, the Python version can be printed by:
```
$ python --version
Python 3.12.0
```
The conda package manager can be used to list the packages installed in a given Miniconda module:
```
$ conda list
```
Available Miniconda environments can be listed by:
```
$ conda info --envs
```
If you need a package which is not available in any of the installed Miniconda
modules or environments, either contact PDC support or follow one of the options described below.

## Activating the base environment
Loading the module does not automatically activate the "base" environment.
To activate the base environment, you can create a script that contains the following
lines

If you save this script as ``conda.init.sh`` and then :
```
$ source conda.init.sh
```
The base environment will be activated, as indicated by ``(base)`` in front of your
bash prompt.

A sample ``conda.init.sh`` file can be found below:

```
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('//pdc/software/23.12/eb/software/miniconda3/24.7.1-0-cpeGNU-23.12/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/pdc/software/23.12/eb/software/miniconda3/24.7.1-0-cpeGNU-23.12/etc/profile.d/conda.sh" ]; then
        . "/pdc/software/23.12/eb/software/miniconda3/24.7.1-0-cpeGNU-23.12/etc/profile.d/conda.sh"
    else
        export PATH="/pdc/software/23.12/eb/software/miniconda3/24.7.1-0-cpeGNU-23.12/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

```

!!! Attention

    If the version of the PDC module or the miniconda3 are changed, please update the conda.init.sh file accordingly.

## Creating your own Python environment
If you create your own conda environment you would have full control and
install everything you would want into that environment. For example
you can create a conda environment under your Klemming folder:
```
ml PDC/<version>
ml miniconda3/24.7.1-0-cpeGNU-23.12
source conda.init.sh
conda create --name my-conda-env
conda activate my-conda-env
conda install <package-name>
```
Please note that by default the conda environment will be stored in the
``.conda`` folder in your home directory. If you would like to store the conda
environment elsewhere, you can use the ``--prefix`` flag to specify the path
when creating the environment.

## Installing your own Miniconda
If you need full control over your Python installation, we recommend that you
install your own Miniconda or Miniconda distribution, which is
relatively easy. The Miniconda
distribution is rather large, while Miniconda is much more lightweight.
Follow these links to find installation instructions for
`Miniconda <https://conda.io/miniconda.html>`_, respectively.

## Installing Python packages using pip
Another option for installing packages which are missing from the available Miniconda
modules (and their conda environments) is to install them locally with `pip`:
```
$ ml PDC/<version>
$ ml miniconda3/24.7.1-0-cpeGNU-23.12
$ pip install --user <package-name>
```
This should install the package locally under ``~/.local/lib/[.....]``.
If you would like to install your local package in a path other than ``~/.local/lib/``,
you can use the ``PYTHONUSERBASE`` environment variable to specify the installation directory
for Python packages that are installed with the ``--user`` flag.

## Using miniconda Python on interactive node
On Dardel, you instead run Python on the allocated interactive node using
the srun command:
```
$ salloc -A <your-project-ID> -t 1:0:0 -n 1 -p shared
$ ml PDC/<version>
$ ml miniconda3/24.7.1-0-cpeGNU-23.12
$ srun -n 1 python some_script.py
```
```
## Using miniconda Python in batch job
#!/bin/bash -l
# The -l above is required to get the full environment with modules
# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A snic20XX-X-XX
# The name of the script is myjob
#SBATCH -J myjob
# Only 1 hour wall-clock time will be given to this job
#SBATCH -t 1:00:00
# Number of tasks
#SBATCH -n 1
# Job partition
#SBATCH -p shared
# load the Miniconda module
ml PDC/<version>
ml miniconda3/24.7.1-0-cpeGNU-23.12
# if you need the custom conda environment:
conda activate my-conda-env
# execute the program
srun -n 1 python some_script.py
# to deactivate the Miniconda environment
conda deactivate
```

## How to use

# Load the Miniconda module
To list all available Miniconda modules on Dardel, type:
```
$ module load PDC
$ module load miniconda3/24.7.1-0-cpeGNU-23.12
```
After loading an Miniconda module, there are information on how to use the Miniconda module:
*JUST LOADING THIS MODULE DOES *NOT* CHANGE THE PYTHON VERSION, NOR ENABLES
ANY EXTRA PYTHON MODULES. This module makes available the 'conda' command, with which users can create named Miniconda environments and then activate them.
To create and use a customized environment use 'conda create ...' and
then 'conda activate ...' (see example below)*.

## Create your own environment
We recommend that you create a ``~/.condarc`` file with the following lines:
```
pkgs_dirs:
- /cfs/klemming/<project>/username/conda-dirs/pkgs
envs_dirs:
- /cfs/klemming/<project>/username/conda-dirs/envs
```
Remember to replace ``<project>`` by your project directory and ``username`` by your username.

Then you can create your own conda environment by the following command.
```
$ mkdir -p /cfs/klemming/<project>/username/conda-dirs/pkgs
$ mkdir -p /cfs/klemming/<project>/username/conda-dirs/envs
$ conda create --prefix /cfs/klemming/<project>/username/conda-dirs/envs/my-conda-env python=3.8
```
Notice that replace ``<project>`` by your project direction and ``username`` by your username as that in the ``~/.condarc``.
After the environment is created you can activate it by:
```
$ conda activate my-conda-env
(my-conda-env)$ python ...
```
To deactivate your environment or the base environment, use ``conda deactivate``.

