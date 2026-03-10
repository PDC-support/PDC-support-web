AlphaFold 3 is an artificial intelligence system developed by Google DeepMind and Isomorphic Labs to predict the three-dimensional structures of biological molecules. Building on earlier versions such as AlphaFold and AlphaFold 2, it extends protein structure prediction to model interactions between proteins, DNA, RNA, and small molecules. This advancement helps researchers better understand biological processes and supports applications in drug discovery and molecular biology.

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
```

You can then use singularity run-help $PDC_SHUB/alphafold3
which will give you commands you can test alphafold with like nvidia-smi, jax-check, jax-run,  etc...
which I have installed in the container.

You can find more about running singularity jobs at
Be aware though that you are running on nvidia and therefore you should use the command

```
srun -n 1 singularity exec --nv -B /cfs/klemming <sandbox folder> <myexe>
```
