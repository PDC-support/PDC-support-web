
# How to login from Linux

## Kerberos based authentication
There are various flavours of Linux and installing the software does differ between distributions.
Configuration of kerberos is however similar in Linux distributions. 
For information on how to login from linux using SSH key based authentication, please refer to [this page](./ssh_login.md#linux-and-macos)

## How to login from Ubuntu Debian

This section describes how to acquire kerberos tickets and login

### Installing Kerberos

In Ubuntu, kinit and ssh are in the packages heimdal-clients and openssh-client.
Install these packages with your favorite package manager or by executing

```default
sudo apt-get install heimdal-clients
sudo apt-get install openssh-client
```

For additional information goto [How to configure kerberos and SSH with kerberos](configuration.md)

## How to login from KTH UBUNTU computers

KTH Ubuntu already has the necessary software and configuration in place, but
the command are working a bit differently so that users can access both
their KTH and PDC home folder.

Most kerberos and ssh commands have a special script starting with **pdc-**
Please not that the PDC password is different from the KTH password.

To acquire a Kerberos ticket

```default
pdc-kinit
```

You can see what active tickets you have by

```default
pdc-klist -f
```

The output of this command should look something like

```default
Credentials cache: FILE:/tmp/krb5cc_2140015_BcRCkm.pdc
Default principal: <your-username>@NADA.KTH.SE

Valid starting       Expires              Flags   Service principal
07/02/2018 11:17:58  07/09/2018 11:17:50  FIA     krbtgt/NADA.KTH.SE@NADA.KTH.SE
07/02/2018 11:43:01  07/09/2018 11:17:50  FIA     afs/pdc.kth.se@NADA.KTH.SE
```

To login into a cluster

```default
pdc-ssh <cluster>.pdc.kth.se
```

Other commands

```default
# Destroy tickets
pdc-kdestroy
# Copy files
pdc-scp <localfile> <username>@t04n28.pdc.kth.se:~/Private/
```

## How to login from Fedora CentOs RHEL

This section describes how to acquire kerberos tickets and login

### Installing Kerberos

For Fedora packages krb5-workstation and openssh-clients are needed.
Install these packages with your favorite package manager or by executing **as root**

```default
yum install krb5-workstation openssh-clients
```

These packages may already be installed. If there are updates available, we recommend you to update it (yum will ask you for it).

Be aware that the MIT kinit shipped with Fedora differs from the Heimdal kinit and that the MIT kerberos library does not
have as many features to break out of firewalls as Heimdal kerberos does.

For additional information goto [How to configure kerberos and SSH with kerberos](configuration.md)

## How to login from SUSE

This section describes how to acquire kerberos tickets and login.

### Installing Kerberos

For SUSE you need to install heimdal and a patched ssh to get GSSAPI-keyExchange to work.
Download and install a suitable rpm from [https://pkgserver.pdc.kth.se/pub/krb/contrib/opensuse/](https://pkgserver.pdc.kth.se/pub/krb/contrib/opensuse/)

Follow instruction for [How to configure kerberos and SSH with kerberos](configuration.md)

You might also need to run the command

```default
/sbin/ldconfig
```

## How to login from other Linux distributions

This section describes how to acquire kerberos tickets and login

### Installing Kerberos

In order to access the computers at PDC in a secure way you have to install some variant of Kerberos binaries.

* Gentoo: Install app-crypt/heimdal and net-misc/openssh
* FreeBSD: generally comes with Kerberos pre-installed (in ports).
* Solaris: At NADA/CSC: module add heimdal/latest, otherwise use the ssh shipped with Solaris.
* Archlinux: Gssapi patch for OpenSSH needed. Either download source code and compile yourself or try this method:

```default
install debtap from AUR //if you are using yaourt use yaourt -S debtap
Download https://packages.debian.org/testing/amd64/openssh-client/download
debtap <package>.deb
sudo pacman -U <package>.pkg
```

If you need support for a Unix dialect that is missing, please [Contact Support](../contact/contact_support.md)
for additional information.

For configure information regarding your setup goto [How to configure kerberos and SSH with kerberos](configuration.md)

* [How to configure kerberos and SSH with kerberos](configuration.md)
  * [Configure Kerberos](configuration.md#configure-kerberos)
  * [Acquire kerberos tickets](configuration.md#acquire-kerberos-tickets)
  * [SSH](configuration.md#ssh)
    * [SSH without configuration](configuration.md#ssh-without-configuration)
    * [SSH with configuration](configuration.md#ssh-with-configuration)
  * [Firewalls and kerberos](configuration.md#firewalls-and-kerberos)
