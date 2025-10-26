TensorFlow™ is an open source software library for machine learning, deep learning
and other numerical computations using data flow graphs. For more information see
the [TensorFlow homepage](https://www.tensorflow.org/).

## How to use
Tensorflow 2.13 is available as a singularity container at PDC.

<!--The container includes TensorFlow 2.13 with support for
AMD GPUs using Rocm-5.7.-->
In order to run the Tensorflow container, first allocate
a GPU node. Then, load the PDC and the singularity
modules.
```
ml add PDC
ml add singularity/4.2.0-cpeGNU-24.11
```
PDC containers are placed at */pdc/software/sing_hub**.
They can also be reached by invoking *PDC_SHUB*.
```
ls $PDC_SHUB
```
Now that singularity is loaded, we can for example open a shell session
within the container with:
```
singularity shell --rocm -B /cfs/klemming /pdc/software/resources/sing_hub/rocm5.7-tf2.13-dev
```
The **--rocm** flag tells singularity to use the GPUs, and the **-B** flag tells singularity to
mount */cfs/klemming* into the container, thereby, making it possible to access files placed outside
it.
After the command, a prompt like this will appear:
```
Singularity>
```
Which means that we are inside the container, and now we can use **python** to run our Tensorflow scripts
from the terminal.
Tensorflow models can also be run directly without the need of opening a shell in the container using
the following command:
```
singularity exec --rocm -B /cfs/klemming /pdc/software/resources/sing_hub/rocm5.7-tf2.13-dev python3 <TF_script.py>
```

## Installing additional Python packages
There are some restrictions regarding singularity on Dardel.
Users cannot write into singularity containers, and therefore,
users cannot install additional python packages directly into the container.

So if you need additional python packages, you can add them via one
of these two following methods:

- Download the Tensorflow singularity container to your local machine where you have a local
installation of singularity. Then, update the image there installing the packages
needed, and afterwards upload the image to Dardel again.
- Install the additional python packages directly on Dardel, but outside the
singularity container. For example, in your home directory (the default behaviour with *pip*),
or in your project directory using the **--target** flag with the *pip* command.
Remember that if you install additional python packages outside the default python
directories, you need to update the **PYTHONPATH** variable with the path where
those new packages are before you run the container.
In this case, the command for launching the shell or running the script directly with the additional packages recognized can be modified as follows:

```
singularity exec --env PYTHONPATH=<.......>:$PYTHONPATH --rocm -B /cfs/klemming /pdc/software/resources/sing_hub/rocm5.7-tf2.13-dev python3 <TF_script.py>
```
This command sets the environment variable PYTHONPATH to include the additional locations where the pacakges are installed outside the container. 

When installing new packages it is advisable to add the condition `numpy==1.22.4` to `pip install` in order to prevent pip from upgrading the version of numpy in the container, which would cause compatibility problems. Example:
```
pip install matplotlib numpy==1.22.4
```
