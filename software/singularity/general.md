
# Singularity

## Instructions for using singularity at PDC

Singularity enables users to have full control of their environment.
Singularity containers can be used to package entire scientific workflows, software and libraries, and even data.
This means that you don’t have to ask your cluster admin to install anything for you -
you can put it in a Singularity container and run. Did you already invest in Docker?
The Singularity software can import your Docker images without having Docker installed or being a superuser.
Need to share your code? Put it in a Singularity container and your collaborator won’t have to go through the pain of installing missing dependencies.
Do you need to run a different operating system entirely?
You can “swap out” the operating system on your host for a different one within a Singularity container.
As the user, you are in control of the extent to which your container interacts with its host.
There can be seamless integration, or little to no communication at all.

More information about singularity can be found at [https://docs.sylabs.io/guides/latest/user-guide/](https://docs.sylabs.io/guides/latest/user-guide/)

## Security

Singularity is more secure on a HPC than other similar solutions like docker or shifter.
Read a comparison about them at [https://hpc.auburn.edu/hpc/docs/hpcdocs/build/html/easley/containers.html](https://hpc.auburn.edu/hpc/docs/hpcdocs/build/html/easley/containers.html). It is important to remember that if you download images they should be trusted
since any container you run will have full access tor your account and your data.

The same goes for images you build yourself, they should be built upon
trusted images.

## Performance

Executing software in containers is very efficient as well as you create
a sandbox of all applications that you do need. Very little performance
loss has been seen.

## Installation of singularity

Singularity is installed as a nosuid on the cluster, meaning that you are
unable to use singularity files, but are able to use
singularity **sandboxes** instead. Otherwise there should be
no difference.
At PDC you cannot write within your containers while being logged
in on the cluster.
Operation for creating containers is better performed on your
local computer.

## How to use singularity on your local computer

### How to install singularity

Singularity can be installed on your computer, with **root access**, so
you can build your own images.
Installation instructions are available at…
[https://docs.sylabs.io/guides/latest/user-guide/quick_start.html#quick-installation-steps](https://docs.sylabs.io/guides/latest/user-guide/quick_start.html#quick-installation-steps)

### Download images from singularity hub

You can find numerous images at [https://singularityhub.github.io/singularityhub-archive/](https://singularityhub.github.io/singularityhub-archive/)
Just download them directly to our file system and use
them for your analysis. The *build* command
in singularity, besides downloading the image, also converts the image to the
latest singularity version.

```text
singularity build --sandbox <sandbox name> shub://<name of image>
```

You can also use images from docker [https://hub.docker.com](https://hub.docker.com)

```text
singularity build --sandbox <sandbox name> docker://<name of image>
```

### Building your own images

Different Linux OS are available for you to download.
At this time the best Ubuntu distribution is available as a
docker image and can be downloaded

```text
sudo singularity build --sandbox <sandbox name> docker://ubuntu:latest
```

Which will download this docker image and convert it into
a sandbox.

### Building your own image from recipes

You can also create an image using a recipe from our PDC github. Singularity recipes with MPI support are available at
[https://github.com/PDC-support/PDC-SoftwareStack/tree/master/other/singularity](https://github.com/PDC-support/PDC-SoftwareStack/tree/master/other/singularity)
In order to create these

```text
sudo singularity build --sandbox <sandbox name> <recipe name>
```

Here is a full example on how to create an image from one of our recipes.

```text
wget https://raw.githubusercontent.com/PDC-support/PDC-SoftwareStack/master/other/singularity/ubuntu-mpich-full.def
sudo singularity build --sandbox ubuntu-full ubuntu-mpich-full.def
```

### Test singularity

With this command you will automatically login into
your singularity image shell.

```text
singularity shell <sandbox name>
```

In the shell you can do the usual Linux shell commands.

### Install software

So now that you do have a sandbox you can start by installing software
in the image. By login into the *writable* sandbox you can use all the commands
that are normal in the operating system, and your internetaccess is
also available in the container, so you can use *wget* or other commands to download data and
softwares. By default on a writable sandbox you login with the user **root**, therefore this should be
executed on your personal computer where you have root access.

```text
sudo singularity shell -w <sandbox name>
```

**Read mode:** You can read/write to file system outside container and
read inside container.

**write mode:** You can read/write inside container. In write mode you are user ROOT, home folder: /root

### Installing the essentials in your image

Although you have downloaded the latest OS, it still
needs some basic software, compilers and libraries.
This can either be installed using a recipe like explained above, or
you can login into your image using **write** mode and install everything you need, for example
updating a sandbox

```text
sudo singularity shell -w ubuntu_sandbox
Singularity> apt-get install update
Singularity> exit
```

### Copying data from local file system to singularity sandbox

You can copy data to your singularity sandbox in several ways.
Either by adding your files into the /root folder in singularity,
and then they will automatically be available in the /root folder
in singularity.

```text
sudo cp <your file> /root
```

You can also bind your folder in singularity.
In order to do that you must bind a folder in singularity to
your local file system. Also the folder in singularity must be created
first. The following example…

1. creates a new folder in the sandbox
1. binds a local folder to that folder
1. logins into the container,
1. copies <files> into your sandbox

```text
sudo singularity exec -w ubuntu_write mkdir <singularity folder>
sudo singularity shell -B <local folder>:/root/<singularity folder> -w ubuntu_write/
Singularity> cp <singularity folder>/<files> .
```

### Where to store runtime files

As the root folder you are login into when using a writable container is
not available using exec from outside the container, if you
plan to run software that you compiled yourself, you must put
the executable somewhere that is accessible by PATH.
 */usr/local/bin* is a good example.
Installed software can then be executed by

```text
singularity exec <sandbox name> <myexe>
```

You can also add a software path in the containers *runscript*
which is a shell file which will be executed when you *run*
the container. The **runscript** file should be stored in
**/.singularity.d/** folder
The script is then executed using

```text
singularity run <sandbox name>
```

### Storing help

help documents on the image should be saved as **runscript.help**
in the folder  */.singularity.d*
This can then be read by

```text
singularity run-help <sandbox name>
```

### Saving your sandbox to PDC cluster

When you are ready installing all the software, paths, folders you
need to transfer your sandbox to the cluster.
To achieve this, it is advisable to first compress it and then transfer it.

```text
sudo tar czf <sandbox name>.tar.gz <sandbox name>
scp <sandbox name>.tar.gz <username>@dardel.pdc.kth.se:/cfs/klemming/home/<u>/<username>
# On Dardel
tar xfp <sandbox name>.tar.gz
```

Another possibility is to transfer a  *.SIF* file to Dardel and convert it to
a sandbox with the *build* command

```text
scp <name>.sif <username>@dardel.pdc.kth.se:/cfs/klemming/home/<u>/<username>
# On Dardel
singularity build --sandbox <sandbox name> <name>.sif
```

Do remember that you do need OpenMPI to execute your software in parallel
on HPC systems. We provide images with OpenMPI installed
in the PDC Hub, but you can also build your own.

## How to remote build a singularity image on the cluster

Instead of running singularity on your local computer as a mean to create a singularity sandbox, you
can instead use the remote build function with a singularity recipy.
Examples of recipies are available at [https://github.com/PDC-support/PDC-SoftwareStack/tree/master/other/singularity](https://github.com/PDC-support/PDC-SoftwareStack/tree/master/other/singularity)
In the description below we use the free service from sylabs for creating sandboxes at PDC.

### Create a sylabs account

In order to be able to get access to the remote building facility you need to
create a free account at [https://cloud.sylabs.io/builder](https://cloud.sylabs.io/builder)

### Create sylabs token

1. Login into sylabs [https://cloud.sylabs.io/builder](https://cloud.sylabs.io/builder)
1. Press **USERNAME -> Access tokens**
1. Enter a name for your *token* and press **Create Access Token**
1. Copy or download the token.

### Adding an access token to the cluster

First of all login to the PDC cluster and access the module singularity

```text
ml PDC/<version>
ml singularity
```

After this run command

```text
singularity remote login
```

The first time you run this command on the cluster, it will save your access token to your profile.
Running the same command again will erase the old token and you can add a new one.

### Remote build a container on the cluster

After having a valid token you can build your singularity sandbox remotely using the command…

```text
singularity build --remote --sandbox <sandbox name> <recipe name>
```

## Create a container at seqera

There are sites where you can build your own singularity container as you see fit by adding which software you
would need and then download the actual singularity container.
Using [seqera](https://seqera.io/containers/) you can choose which software you want to use, and then download a container created for this purpose.

## Running singularity images at PDC

Singularity works on Dardel by loading the singularity module.
There are however restrictions. As explained above you are not able to write
into singularity container. You are however able to build singularity sandboxes from
containers available online, but not from recipes.

```text
singularity build --sandbox <sandbox name> docker://ubuntu:latest
```

Also, you are able to *run*, *run-help*, *exec*, *shell*, as well as other
non-write commands, on singularity sandboxes at PDC.

Below are a couple of example on how to run a singularity container on PDC systems.
As the Lustre filesystem is not recognised by default it is important to bind said filesystem, which
is done in the example scripts below.

### Ready made containers at PDC

PDC provides some default containers for testing and certain software which are placed
at **/pdc/software/sing_hub**
These can also be reached by invoking  *$PDC_SHUB*

```text
ls $PDC_SHUB
```

As highlighted before these containers are built as a *sandbox* and can be run with our clusters.
In order to get information about what they contain please run

```default
singularity run-help $PDC_SHUB/<sandbox name>
```

Recipes on how several of these container are bult is available at [https://github.com/PDC-support/PDC-SoftwareStack/tree/master/other/singularity](https://github.com/PDC-support/PDC-SoftwareStack/tree/master/other/singularity)

### Job scripts

Follow information on how to create Job scripts at this page, which is not covered below.
Although here are a couple of examples on how to run jobs on the dardel cluster.

#### Batch job without MPI

In case you would like to run on one node you do not need MPI support
in your image and you can send in a job using…

```text
#!/bin/bash -l
# The -l above is required to get the full environment with modules
# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A 201X-X-XX
# The name of the script is myjob
#SBATCH -J myjob
# Only 1 hour wall clock time will be given to this job
#SBATCH -t 1 00 00
# Number of nodes
#SBATCH --nodes=1
# Using the shared partition as we are not using all cores
#SBATCH -p shared
# Number of MPI processes per node
#SBATCH --ntasks per node=24
# Run the executable named myexe
ml PDC/<version> singularity
srun -n 24 singularity exec -B /cfs/klemming <sandbox folder> <myexe>
```

#### Batchjob with MPI

In case you need to parallelize your software across nodes you should use one of the
recipes with Cray MPI support mentioned earlier which do reside in the [https://github.com/PDC-support/PDC-SoftwareStack](https://github.com/PDC-support/PDC-SoftwareStack)

```text
#!/bin/bash -l
# The -l above is required to get the full environment with modules
# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A 201X-X-XX
# The name of the script is myjob
#SBATCH -J myjob
# Only 1 hour wall clock time will be given to this job
#SBATCH -t 1 00 00
# Number of nodes
#SBATCH --nodes=2
# Using the shared partition as we are not using all cores
#SBATCH -p shared
# Number of MPI processes per node
#SBATCH --ntasks per node=12
# Run the executable named myexe
ml PDC/<version> singularity
srun -n 24 --mpi=pmi2 singularity exec -B /cfs/klemming <sandbox folder> <myexe>
```

#### Batch job with GPU support

In case you would like to run on one node with AMD GPUs.
Be aware that you need a container with software compilated
using GPU support. Look at our [https://github.com/PDC-support/PDC-SoftwareStack](https://github.com/PDC-support/PDC-SoftwareStack)
for recipes on how to build.
in your image and you can send in a job using…

```text
#!/bin/bash -l
# The -l above is required to get the full environment with modules
# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A 201X-X-XX
# The name of the script is myjob
#SBATCH -J myjob
# Only 1 hour wall clock time will be given to this job
#SBATCH -t 1 00 00
# Number of nodes
#SBATCH --nodes=1
# Using the GPU partition which is at the moment is under testing
#SBATCH -p gpu
# Run the executable named myexe
ml PDC/<version> singularity
srun -n 1 singularity exec --rocm -B /cfs/klemming <sandbox folder> <myexe>
```
