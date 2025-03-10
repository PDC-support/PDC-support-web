The DIRAC program computes molecular properties using relativistic quantum
chemical methods. It is named after P.A.M. Dirac, the father of relativistic
electronic structure theory.
For more information see: http://diracprogram.org


## How to use

To run DIRAC we need two input files (one file for the job specification
and one file to specify the molecule). In addition
we need a run script.
To have a simple and quick toy example we will calculate the HF energy of
methanol. This calculation takes only few seconds to run.
We will use the following job specification (scf.inp):
together with the following molecule specification (methanol.xyz):
and the following example runscript (dirac.run):
Here we run on 1 node (32 processors in total).
Do not run serial calculations on Beskow for anything other than small tests!
Now we are ready to submit the calculation
```
$ sbatch dirac.run
```
