MMseqs2 (Many-against-Many sequence searching) is a GPU-accelerated software suite designed for searching and clustering very large protein and nucleotide sequence datasets. It can run up to 10,000 times faster than BLAST, while still maintaining nearly the same sensitivity at 100-fold speed. Additionally, it performs profile searches with sensitivity comparable to PSI-BLAST, but at more than 400 times the speed.
More information at https://github.com/soedinglab/MMseqs2

## How to use

In order to run it you must use the dardel-gh nodes.
In order to check it out use

```
ssh dardel.pdc.kth.se
ssh logingh
ml PDC
ml mmseq2-gpu
```

### Setting the GPUs

MMseqs2 can use 1 or more GPUs for its calculation.
These can be set with the variable `CUDA_VISIBLE_DEVICES=<N> ...`
Where **N** is the GPU number.
If this is omitted ALL available GPUs will automatically be used.
As this is a hybrid code, it will use both CPU and GPUs available.
For best performance, use the values in the table below.

On Dardel

| N GPUs | Value | threads |
|---|---|---|
| 1 | 0 | 8 |
| 2 | 0,1 | 16 |
| 3 | 0,1,2 | 24 |
| 4 | 0,1,2,3 | 32 |

### Types of alignment modes

By default MMseq2 just finds candidate matches using k-mers and fast heuristics, computes scores and E-values
but does NOT compute a residue by residue alignment.
If you want full Smith-Waterman alignment which is comparable as used by blast you should
add parameter `--alignment-mode 3` although this type of mode is considerably slower.

## How to run

For running the alignment there are a couple of pre/post commands that need to be
executed.

### Creating your target

First of all you need to create a FASTA format file with the sequence you want to
search for. This file needs to be converted to adapt to MMseq2
```
mmseqs createdb [fasta source] [seqDB]
```
This creates several files starting with the name **[seqDB]**

### Send in a batch job

This is an example that uses Full Smith-waterman alignment on 2 GPUs, optimized threads
against the **NR** database and searches for **seqDB**

```
#!/bin/bash -l
#SBATCH -A [Allocation]
#SBATCH -p gpugh
#SBATCH -J [Name]
#SBATCH -t [Time]
#SBATCH --nodes=1

ml PDC
ml mmseq2-gpu
export CUDA_VISIBLE_DEVICES=0,1
srun -n 1 mmseqs search [seqDB] /sw/data/MMseqs2_gpu_data/NR [results_nr] $NAISS_TMP -a --alignment-mode 3 --gpu 1 --threads 16
```

After this job has been executed you should see several files with the name **[results_nr]**

### Creating human readible results

You need to convert the results in human readibly format which is similar
to the blast output

```
mmseqs convertalis [seqBD] /sw/data/MMseqs2_gpu_data/NR [results_nr] [hits_with_sequences.tsv] --format-output "query,target,evalue,bits,pident,alnlen,qaln,taln"
```

This will create one file **[hits_with_sequences.tsv]** containing the results, with alignment.
