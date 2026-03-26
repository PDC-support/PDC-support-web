NVIDIA Parabricks is a high-performance software suite designed to accelerate genomic data analysis. It provides GPU optimized versions of widely used bioinformatics tools, allowing researchers to process sequencing data much faster compared to traditional CPU based workflows.

Many common bioinformatics tools such as those used for alignment, variant calling, and data preprocessing have been adapted within Parabricks to run efficiently on NVIDIA GPUs. By leveraging the parallel processing power of GPUs, these tools can achieve significant speedups while maintaining the same results as their standard implementations.

This makes Parabricks especially useful for large-scale genomics projects, where reducing analysis time can greatly improve productivity and enable faster scientific discoveries.

For a full overview of what softwares are included please read the information at [Parabricks](https://docs.nvidia.com/clara/parabricks/latest/softwareoverview.html)

## How to use

Parabricks is only available via the GraceHopper nodes on Dardel and can be used via
a singulary container

In order to use you need to run the following commands...

```
ssh dardel.pdc.kth.se
ssh logingh
ml PDC
ml singularity
ml nvidia
```

After this you can use the following commands to test its functionality

`singularity run --nv $PDC_SHUB/clara-parabricks_4.7.0-1 pbrun --help`

`singularity run --nv $PDC_SHUB/clara-parabricks_4.7.0-1 pbrun version`

To test the GPUs...
`singularity exec --nv $PDC_SHUB/clara-parabricks_4.7.0-1 nvidia-smi`

## How to run

There is a test dataset available which you can find at `$PDC_SHUB/parabricks_sample`

Here is a quick example that you can run on 1 gpu
```
singularity exec --nv -B $PDC_SHUB/parabricks_sample:/data \
    $PDC_SHUB/clara-parabricks_4.7.0-1 \
    pbrun fq2bam \
    --ref /data/Ref/Homo_sapiens_assembly38.fasta \
    --in-fq /data/Data/sample_1.fq.gz /data/Data/sample_2.fq.gz \
    --out-bam fq2bam_output.bam \
    --num-gpus 1
```

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
srun -n 1 singularity exec --nv -B $PDC_SHUB/parabricks_sample:/data \
    $PDC_SHUB/clara-parabricks_4.7.0-1 \
    pbrun fq2bam \
    --ref /data/Ref/Homo_sapiens_assembly38.fasta \
    --in-fq /data/Data/sample_1.fq.gz /data/Data/sample_2.fq.gz \
    --out-bam fq2bam_output.bam \
    --num-gpus 4
```
