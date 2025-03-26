

# Scania

This page contains useful information for users from SCANIA.

## Get an account

To get started using PDC resources within the Scania collaboration,
please begin by applying for an account at [https://blackfish.pdc.kth.se/cgi-bin/accounts/request.py](https://blackfish.pdc.kth.se/cgi-bin/accounts/request.py)
Specify that you want to use the system Dardel and add a comment saying that your are
part of the Scania collaboration at PDC.
Once we have received your application we will confirm that you are indeed a Scania user,
and will proceed in creating an account for you.

## Login

Once you have received your PDC account letter you may login at PDC.
To connect to PDC from within Scania you first need to contact Scania IT
to have your computer activated for PDC access.
Instructions on how to configure your computer for
PDC access can be found by following these instructions on [How to log in with kerberos](../login/kerberos_login.md#how-to-log-in-with-kerberos)

## Dardel

When accessing Dardel always login to the Scania dedicated login node

```default
dardel-scania.pdc.kth.se
```

## Login commands

First generate a Kerberos ticket as follows where you should
substitute *username* with your username at PDC…

```default
kinit -l 30d <username>@NADA.KTH.SE
```

Once you have a valid ticket you can ssh to **dardel-scania.pdc.kth.se** using

```default
ssh -K <username>@dardel-scania.pdc.kth.se
```

Read more information on how to login with [How to log in with kerberos](../login/kerberos_login.md#how-to-log-in-with-kerberos)

## File transfer

Files are transferred with scp from PDC to Scania as follows:

```default
scp <username>@dardel-scania.pdc.kth.se:<filename> .
```

Read more information about [Using scp/rsync](../data_management/file_transfer_scp.md#using-scp-rsync)

## Storage

Scania has its own dedicated Lustre disk system, which is available from Dardel

```default
/cfs/scania
```

Every scania user has their homedirectory at

```default
/cfs/scania/home/<1st letter username>/<username>
```

where **u** is the first letter of your PDC **username**.
You should always execute your programs in the parallel file system (Lustre).
Read more information in the following [Storage areas](../data_management/klemming.md)

## How to use Linux

You can find a short tutorial on how to use Linux and
how to set file permissions by reading [Basic Linux for new HPC users](../basics/introduction.md#basic-linux-for-new-hpc-users)

## Software

As a SCANIA user you should mainly be interested in…

* PowerFLOW
* OpenFOAM
* StarCCM+

PDC does also other applications.
Please take a look at [https://www.pdc.kth.se/software](https://www.pdc.kth.se/software)
for a list of softwares available at PDC.

## Mailing list

Scania users are automatically added to the mailing list:

```default
scania-users@pdc.kth.se
```

Both PDC staff and Scania users may post to this list
to quickly distribute important information for Scania users.

## Contact support

Scania has its personal support queue at PDC which can be
reached by sending mails to

```default
scania-support@pdc.kth.se
```

More information on how tickets are handled and
some general contact information can be found at [Contact Support](../contact/contact_support.md)
