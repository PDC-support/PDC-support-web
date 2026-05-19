Ansys/CFX is a computational fluid dynamics (CFD) software. As of 2012 KTH have made a joint purchase of ANSYS (in which CFX is one component).

# How to use Ansys/CFX on PDC machines
In order to use ANSYS CFX at PDC you need to:
1. Have an account at PDC.
2. Check with the Ansys license owner at your department to allow running Ansys/CFX at PDC
3. Contact KTH if you have problems/questions with Ansys/CFX licenses.
Use command
module load PDC
module avail cfx
to list all available versions and make sure that the correct version is loaded in the job script. If there is no same (compatible) versions, please contact PDC using the link [https://supr.naiss.se/support/?centre_resource=c7](https://supr.naiss.se/support/?centre_resource=c7).
For more details, look at Ansys web page:
http://www.ansys.com/


## How to use


# Submitting a CFX job on Dardel
**Important note: Due to some technical issues, only single-node computations are possible (every node has 128 cores).We are working on the problem and will update this page once we fix the problem.**
A script for running Ansys/CFX on Dardel called cfx_run.sh is shown below.
and submit it from Dardel's login node
sbatch cfx_run.sh
Note that this script does not contain all the options for CFX. You may want to add more options depending on your job.

