PyTorch is an open-source machine learning library for Python, based on Torch.
PyTorch provides two high-level features:
- Tensor computation (like NumPy) with strong GPU acceleration
- Deep neural networks built on a tape-based autodiff system


## How to use


# Instructions for using pytorch at PDC
PyTorch is installed as a singularity container at PDC.
The container includes PyTorch 1.13.0 with support for
AMD GPUs using Rocm-5.4.
In order to run the PyTorch container, first allocate
a GPU node. Then, load the PDC and the singularity
modules.
ml add PDC/22.06
ml add singularity/3.10.4-cpeGNU-22.06
PDC containers are placed at */pdc/software/sing_hub**.
They can also be reached by invoking *PDC_SHUB*.
ls $PDC_SHUB
Now that singularity is loaded, we can for example open a shell session
within the container with:
singularity shell --rocm -B /cfs/klemming /pdc/software/resources/sing_hub/rocm5.4_ubuntu20.04_py3.8_pytorch
The **--rocm** flag tells singularity to use the GPUs, and the **-B** flag tells singularity to
mount */cfs/klemming* into the container, thereby, making it possible to access files placed outside
it.
After the command, a prompt like this will appear:
Singularity>
Which means that we are inside the container, and now we can use **python** to run our PyTorch scripts
from the terminal.
PyTorch models can also be run directly without the need of opening a shell in the container using
the following command:
singularity exec --rocm -B /cfs/klemming /pdc/software/resources/sing_hub/rocm5.4_ubuntu20.04_py3.8_pytorch python3 <pytorch_script.py>

## Installing additional Python packages
There are some restrictions regarding singularity on Dardel.
Users cannot write into singularity containers, and therefore,
users cannot install additional python packages directly into the container.
So if you need additional python packages, you can add them via one
of these two following methods:
- Download the PyTorch singularity container to your local machine where you have a local
installation of singularity. Then, update the image there installing the packages
needed, and afterwards upload the image to Dardel again.
- Install the additional python packages directly on Dardel, but outside the
singularity container. For example, in your home directory (the default behaviour with *pip*),
or in your project directory using the **--target** flag with the *pip* command.
Remember that if you install additional python packages outside the default python
directories, you need to update the **PYTHONPATH** variable with the path where
those new packages are before you run the container.
