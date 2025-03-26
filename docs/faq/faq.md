

# Frequently Asked Questions (FAQ)

## Filesystem

### I get “Disk quota exceeded” in my project directory even though the storage quota is not full

You can use the `projinfo` command to check the usage of your home directory quota in addition to all the other allocations you are part of. Please check that the storage usage in the home as well as projects directories is under the limit in terms of both the number of files as well as the storage size. Furthermore, you can also check individual quotas as described below.

Check your project quota with:

```default
lfs quota -hp `stat -c "%g" /cfs/klemming/projects/snic/my_project` /cfs/klemming
```

Check your personal quota with:

```default
lfs quota -hp $UID /cfs/klemming
```

### How can I share files with PDC support?

By default only you have access to your files. But when in contact with support it can be useful to share log files, Makefiles, source code, core files etc. There are different ways to do this

1. Copy the files to your public directory. The public directory is a space in your home directory where everyone has read access. This method is best for small data that is okay to share with all users of the system.
```default
cp my_file $HOME/Public
cp -R my_directory $HOME/Public
```

1. Give access permission to the files directly. We provide the command `support-access` to do this automatically (by setting up [Access Control Lists](../data_management/klemming.md#access-control-lists)). This method works even for large data, and gives access only to PDC staff. It does not work in project directories.
```default
support-access my_file
support-access my_directory
```

## Kerberos

### I got “kinit  krb5 get init creds No ENCTS found” error when trying to run kinit.

Contact PDC support using the link https://supr.naiss.se/support/?centre_resource=c7 to request an extention of your Kerberos principal. When this has been done you can
continue to login again using the same password as you did before. If you do not have a valid time allocation this will not be done.

### How do I reset my Kerberos password?

If you remember your current Kerberos password (i.e. your password to log in to PDC) and would like to reset it,  you can do so using the `kpasswd` command.
Just type the command into a terminal and you will be prompted for your old password, and then asked to type
your new password twice.

If you don't recall your current password, and would like to receive a new one, please submit this form [PDC new password request](https://blackfish.pdc.kth.se/cgi-bin/accounts/password.py)

### I got “krb5 cc new unique  Credentials cache file permissions incorrect” error when trying to run kinit

Please check the output of *klist* command as there may be conflict between Kerberos tickets for different realms.
Try *kdestroy* and then *kinit* again to get Kerberos ticket for NADA.KTH.SE.

For Windows users: If the error persists, please use [Network Identity Manager](https://www.secure-endpoints.com/netidmgr/)
to manage Kerberos tickets. Remember to set default identity by right-clicking the Kerberos principal ending with NADA.KTH.SE,
and choosing the *Set as default* menu item.

### When using the KTH Ubuntu computers I lose permission to access my documents after getting my Kerberos ticket

Both PDC systems and KTH Ubuntu systems use Kerberos authentication, but are in different realms.
Replacing the login session’s credentials with PDC credentials will destroy the access to your AFS home directory,
typically causing applications or the entire login session to crash.

A workaround to the issue is to use pdc-\* in front of the commands needed to access PDC systems.
This includes: kinit, klist, kdestroy, ssh, scp… The new commands would then be  *(pdc-kinit, pdc-klist, pdc-kdestroy, pdc-ssh, pdc-scp)*.
These commands work in the same way as the original commands, but stores/looks for the Kerberos ticket in a different location.

### Kerberos tickets without address

If you get the error message when you connect to PDC

```default
kinit: krb5_get_init_creds: Incorrect net address
```

or

```default
Kerberos V5 refuses forwarded credentials because Read forwarded creds failed: Incorrect net address
```

this is a sign that you are sitting behind NAT. NAT stands for Network Address Translation and is used when you
have several computers (for instance at home) who all have addresses on an internal network but are connected through
the same router/base station/broadband modem and for someone looking from the outside behave as if they
had been assigned the same address from the internet provider.

That the Kerberos-server (i.e. the Kerberos KDC: Key Distribution Center) complains about “Incorrect net address”
is because kinit creates an address with your computers internal address - but seen from the KDC it looks like your
computer has the address of the NAT that you are behind.

To resolve this, first try asking for addressless tickets from Kerberos, that is use

```default
kinit --forwardable --no-addresses <username>@NADA.KTH.SE
```

This can be made default for your computer by adding the following to your Kerberos configuration file,
krb5.conf:

```default
[appdefaults]
no-addresses = yes
```

See more information at [Firewalls and kerberos](../login/configuration.md#firewalls-and-kerberos)

### kinit  krb5 get init creds  Incorrect net address

This is most likely caused by a NAT firewall (such as a wideband router used for most home connections).

**Remedy:** Go to [Firewalls and kerberos](../login/configuration.md#firewalls-and-kerberos) and try the –no-addresses option to kinit or –extra-addresses=xyz.xyz.xyz.xyz with xyz replaced by the IP number of your external NAT interface. This page should give you the address of the external NAT interface in most (but not all) cases.

### Kerberos V5 mk req failed Server not found in Kerberos database

This is most often caused by a malfunctioning name server (such as the ones provided by some home consumer ISPs)

**Remedy:** You will need to add a file krb5.conf which contains a section [domain_realm] with the correct Kerberos realm information and you will need to use an environment variable to tell Heimdal the name of your config file is (if it is not /etc/krb5.conf). Add this content in the krb5.conf file:

```default
[domain_realm]
  .nada.kth.se = NADA.KTH.SE
  .pdc.kth.se = NADA.KTH.SE
```

### kinit  krb5 get init creds  unable to reach any KDC in realm NADA KTH SE

If you get this error message you are most probably behind a firewall that blocks communication with our Kerberos servers.

**Remedy:** Go to [Firewalls and kerberos](../login/configuration.md#firewalls-and-kerberos).

### Cannot find KDC for requested realm while getting initial credentials

Again this likely due to a firewall.

**Remedy:** Go to [Firewalls and kerberos](../login/configuration.md#firewalls-and-kerberos).


### Time is out of bounds

If this happens you probably have time synchronization problem:

```default
./kinit
<username>@NADA.KTH.SE's Password:
kinit: Time is out of bounds (krb_rd_req)
```

This problem is caused by lack of synchronization between the system you create your Kerberos ticket on and the one you try to login on using that Kerberos ticket. Kerberos demands a maximum of 5 minutes time difference between the system clocks.

**Remedy:**
There are a number of methods to synchronize clocks between machines. The one we recommend is NTP, a
protocol for synchronizing clocks over the internet.
[Information and software for NTP can be found online.](http://www.ntp.org/)
If everything looks right, but it does not work anyway, your computer is probably
set up for the wrong timezone or the wrong daylight savings time period.

### kinit  krb5 get init creds  time skew  370  larger than max  300

This is again caused by the clock on your system being out of sync with the actual time.

**Remedy:** See information under [Time is out of bounds](#time-is-out-of-bounds).

### kinit  krb5 get init creds  Clock skew too great Unable to negotiate a key exchange method

This is again caused by the clock on your system being out of sync with the actual time.

**Remedy:** See information under [Time is out of bounds](#time-is-out-of-bounds).

### kinit tcp unknown service  using default port 2120

This is not an error message and has no impact on the functionality of Kerberos under normal circumstances. The message informs the user that the kauth/tcp system service is not registered in the client machine as a known service with an assigned port number. The kauth client program therefore selects the default “standard” connection port 2120 when talking to the PDC Kerberos server. This is the wanted behavior.

On most systems the information where the service to port look up table is located is the file /etc/services. Note that other Kerberos client programs (kx, telnet, rsh) may produce similar messages, but may use other port numbers than 2120 as the correct default.


### Client's entry in database has expired

This message indicates that your Kerberos principal has expired. This happens automatically every other year and means that you can not get any Kerberos tickets and therefore you can not login at PDC.

**Remedy:** Write an e-mail asking PDC support to extend your Kerberos principal. When this has been done you can continue to login again using the same password as you did before.


## Login

### When obtaining Kerberos credentials I get the error “Preauthentication failed”

This usually means that the wrong passwords was entered. Please double check
that you have entered the correct password for your PDC account. If this still
fails, please see [I forgot my password, how can I get a new one?]()

### I forgot my password  how can I get a new one?

You can request a new password using our [online form](https://blackfish.pdc.kth.se/cgi-bin/accounts/password.py). The form requires you
to submit a copy of a valid ID card or passport. We will send you the new
via an encrypted link.

### I cannot login but have valid Kerberos

This can either be that you are not allowed to log in since you are
not part of an active time allocation at PDC, or there is an error in your
configuration files.
First of all you should check if you are part of a time allocation on the
cluster you are trying to log in to by looking it up on SUPR (if your project is managed through SUPR), or by asking your principal investigator/Course
administrator if you have been added as a member to the time allocation.
If you are a member of an active time allocation there could be
some problems with your configuration files.
To troubleshoot configuration file problems please try to log in manually…

```default
ssh -vvv -o GSSAPIAuthentication=yes <username>@<cluster>.pdc.kth.se
```

If this works, the original problem was probably caused by errors in the ssh configuration file.

In order to know what ssh you are using on your computer, you can
execute

```default
which ssh
```

### I have a PDC account and want to link it to my SUPR account

Most projects are now managed through SUPR, and in this case your PDC accounts should be linked to a SUPR account.
This will facilitate your automatic membership at PDC to projects that are available in SUPR.
If you applied for an PDC account outside of SUPR, your account might not be linked.
You should check if your SUPR and PDC accounts are linked and, if necessary, arrange for the accounts to be linked.

To link your SUPR account to your PDC account…

Contact PDC support requesting that your PDC account be linked to your SUPR account. Include the following details in your email:

1. Your PDC username
1. Your SUPR account ID (At the top of your personal page)
1. E-mail address connected to your SUPR account

PDC Support will send you a confirmation email when your SUPR account has been linked to your PDC account.

## Running

### Job submit allocate failed Invalid partition or qos specification

Usually this depends on user not adding time allocation, or adding it wrongfully. Using *salloc*
you should use *-A <allocationid>* and for batch files:

```default
#SBATCH -A <allocationid>
```

You can check the time allocations you are a member of with

```default
projinfo [options]
```

### Job submit allocate failed  No partition specified or system default partition

In this case you have not selected which partition your job should be running on.
Using *salloc*
you should  *-p <partition>* and for batch files:

```default
#SBATCH -p <partition>
```

Here is a complete list of all [Dardel partitions](../run_jobs/job_scheduling.md#dardel-partitions)

### I want to test PDC resources and check if it suits my needs

If you want to try out PDC resources to make sure it suits your needs, you will need to apply for a PDC account and
choose time allocation: pdc-test-xxxx , the last one being the current year. By doing that you will be able to submit
your jobs for an specific period of time and check if it fits your needs.

If you decide to run using PDC resources you
will then need to apply for a time allocation for yourself.

!!! note 

  This is only a test allocation and has very limited amount of corehours

### I do not get any e-mails when my job is started finished

By default SLURM send a an e-mail when your job has started/finished
and if you do not have entered any e-mail address in your script,
SLURM will automatically send it to the address in  *.forward*
so it is important that you see that this file has an updated e-mail.

This file resides in

```default
/cfs/klemming/home/<first letter username>/<username>/Public/.forward
```

In order to change your e-mail address you can write

```default
echo "<YOUR NEW E-MAIL>" > /cfs/klemming/home/<first letter username>/<username>/Public/.forward
```

### Problems to run multiple jobs or srun steps at the same time on a compute node

When running multiple jobs on a shared node or multiple srun-steps on a full compute node, the variable
`FI_CXI_DEFAULT_VNI` needs to be set before launching an executable with srun.

```default
export FI_CXI_DEFAULT_VNI=$(od -vAn -N4 -tu < /dev/urandom)
```

## Other

### Problems with the cluster

In case of cluster errors, or unavailability, news regarding its status are also available at [https://www.pdc.kth.se/cgi-bin/flash/flash.py](https://www.pdc.kth.se/cgi-bin/flash/flash.py)
