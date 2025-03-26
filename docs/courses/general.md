

# General instructions for PDC courses

## Get an account

Before your course/workshop starts, all participants need to have a PDC account.
Please visit [https://blackfish.pdc.kth.se/cgi-bin/accounts/request.py](https://blackfish.pdc.kth.se/cgi-bin/accounts/request.py) and request an account
**at least one week before the workshop starts**.
Specify which course/workshop you will be participating in.
Once we have received your application we will confirm that you are indeed registered
for the workshop and create an account for you.

## How to use Linux

You can find a short tutorial on how to use Linux by reading [Basic Linux for new HPC users](../basics/introduction.md#basic-linux-for-new-hpc-users).

## Preparing for login

Once you have received your PDC account letter you may login at PDC.
General instructions on how to configure your computer for
PDC access can be found by following the instructions on [How to log in with kerberos](../login/kerberos_login.md#how-to-log-in-with-kerberos).
Step-by-step guides are available for [How to login from Linux](../login/linux_login.md), [How to login from Mac OS](../login/mac_login.md) and [How to login from Windows](../login/windows_login.md).

If the lab exercises you are participating in take place in a computer lab room at KTH which have
Ubuntu desktop computers, you are already set up for PDC access. Specific instructions
are available for [How to login from KTH UBUNTU computers](../login/linux_login.md#how-to-login-from-kth-ubuntu-computers).

## Login to Dardel

[Dardel](https://www.pdc.kth.se/hpc-services/computing-systems/about-dardel-1.1053338) is a
Cray EX supercomputer which is used for the MPI, OpenMP and Performance Engineering
computer labs. Each node on Dardel is equipped with 2 AMD EPYC 2.25 GHz 64 core processors, thus providing 128 physical cores on each node.

To log in to Dardel type

```default
$ ssh <username>@dardel.pdc.kth.se
```

or, if using a KTH-Ubuntu computer,

```default
$ pdc-ssh <username>@dardel.pdc.kth.se
```
