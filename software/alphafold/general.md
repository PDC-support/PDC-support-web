AlphaFold 3 is an artificial intelligence system developed by Google DeepMind and Isomorphic Labs to predict the three-dimensional structures of biological molecules. Building on earlier versions such as AlphaFold and AlphaFold 2, it extends protein structure prediction to model interactions between proteins, DNA, RNA, and small molecules. This advancement helps researchers better understand biological processes and supports applications in drug discovery and molecular biology.
For information about how to run alphafold3, and for setting its parameters, is available at
https://deepwiki.com/google-deepmind/alphafold3/3-user-guide

## How to use

Due to incompatibility with ARM64 CPUs, alphafold3 was installed without support
for Triton.

In order to run it you must use the dardel-gh nodes.
In order to check it out use

```
ssh dardel.pdc.kth.se
ssh logingh
ml PDC
ml singularity
ml nvidia
```

You can then use singularity run-help $PDC_SHUB/alphafold3
which will give you commands you can test alphafold with like nvidia-smi, jax-check, jax-run,  etc...

To test the GPUs...
`singularity exec --nv $PDC_SHUB/alphafold3 nvidia-smi`

### Setting the GPUs

Alphafold can use 1 or more GPUs for its calculation.
These can be set with the variable `XLA_VISIBLE_DEVICES=<N> ...`
Where **N** is the GPU number.
If this is omitted ALL available GPUs will automatically be used.

On Dardel
| N GPUs | Value |
|---|---|
| 1 | 0 |
| 2 | 0,1 |
| 3 | 0,1,2 |
| 4 | 0,1,2,3 |

### To test singularity
This is a simple test to check alphafold on 1 GPU

`CUDA_VISIBLE_DEVICES=0 singularity exec --nv $PDC_SHUB/alphafold3 jax-check`

### How to run

In general on dardel you can run it for 1 GPU like...
```
CUDA_VISIBLE_DEVICES=0 singularity exec --nv -B \
    [DATA FOLDER]:/input \
    -B [DATA FOLDER]:/output \
    $PDC_SHUB/alphafold3 python3 /opt/alphafold3/run_alphafold.py \
    --json_path=/input/config.json \
    --output_dir=/output
```

Where the **[DATA FOLDER]** contains information about the json file/input/output data. See documentation for alphafold3.

## Send in a batch job

In order to use all GPUs on a node you need to send in a batch job.
here is the same example using all GPUs on an exclusive node

```
#!/bin/bash -l
# Set the allocation to be charged for this job
#SBATCH -A naissYYYY-X-XX
# The name of the script is myjob
#SBATCH -J myjob
# The partition
#SBATCH -p gpugh
# 1 hour wall clock time will be given to this job
#SBATCH -t 01:00:00
# Number of nodes
#SBATCH --nodes=1
ml PDC
ml singularity
ml nvidia
CUDA_VISIBLE_DEVICES=0,1,2,3 singularity exec --nv -B \
    [DATA FOLDER]:/input \
    -B [DATA FOLDER]:/output \
    $PDC_SHUB/alphafold3 python3 /opt/alphafold3/run_alphafold.py \
    --json_path=/input/config.json \
    --output_dir=/output
```

Where the **[DATA FOLDER]** contains information about the json file/input/output data. See documentation for alphafold3.
