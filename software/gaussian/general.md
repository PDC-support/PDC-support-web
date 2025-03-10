`Gaussian <http://www.gaussian.com>`_ is a commerical electronic struture
modelling program. Users need to provide their own license to
use Gaussian at PDC resources.


## How to use


# Example input: Structure optimization of benzene with B3LYP functional
To give an explicit example we will optimize the structure of benzene using the B3LYP functional with the following input file (we call it benzene.com):
:language: text
Please note that there is one blank line at the end of the input. If you forget
this blank line you will see an error termination with the error
```
End of file in ZSymb.
```

## Parallelization using OpenMP
At PDC we do not hold a license for Linda parallelization of Gaussian, so only
single node jobs can be run. Intra-node parallelism is achieved using OpenMP. The number of cores that are used by Gaussian
can be changed using the %NProcShared Link 0 command.

## Submitting the job
To submit a Gaussian job we use the following run script (we call it gaussian.run):
:language: text
Having the input file (benzene.com) and the run script (gaussian.run), we are ready to submit the job
```
$ sbatch ./gaussian.run
```
This calculation only takes few minutes. A successful
calculation will terminate with a line that looks like this one
```
Normal termination of Gaussian 09 at Tue Sep 22 15:39:26 2015.

```
