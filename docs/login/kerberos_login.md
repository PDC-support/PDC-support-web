

# How to log in with kerberos

This section covers the procedure for accessing PDC resources. Before following this section,
make sure you have a PDC account successfully created and you have recieved your username and password.

In order to log in to PDC computers you require:

1. A Kerberos installation
1. A SSH implementation that supports Kerberos.

Logging into PDC is a two stage process. You must first generate Kerberos credentials using kinit,
which requires a password, then use those credentials together with SSH to log in to cluster
on which you have an active allocation.

## General information about Kerberos

PDC uses [Kerberos](http://web.mit.edu/kerberos/) authentication protocol.

![alternate text](https://pdc-web.eecs.kth.se/files/support/images/login.png)

Kerberos tickets are stored on your local machine, and are then forwarded when you try to log in to the remote system.
You’ll need the following software in versions that are appropriate for your operating system:

* Kerberos v5 software (from Heimdal) - which is necessary for getting a Kerberos ticket, and

### Commonly used Kerberos commands

Here is a list of commonly used kerberos commands for users.

| Command   | Description                                                                                                                                                                                                                                         |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| kinit     | kinit obtains and caches an initial ticket-granting ticket for principal.<br/>Usage `kinit -f [username]@NADA.KTH.SE`                                                                                                                               |
| klist     | klist lists the Kerberos principal and Kerberos tickets held in a<br/>credentials cache, or the keys held in a keytab file.                                                                                                                         |
| kdestroy  | The kdestroy utility destroys the user’s active Kerberos authorization<br/>tickets by overwriting and deleting the credentials cache that contains them.<br/>If the credentials cache is not specified, the default credentials cache is destroyed. |
| kpasswd   | The kpasswd command is used to change a Kerberos principal’s password.<br/>kpasswd first prompts for the current Kerberos password,<br/>then prompts the user twice for the new password, and the password is changed.                              |

## Login nodes

On our clusters we have several login nodes. A main one and one node used as backup in case the first one
is out of commission.
The login nodenames uses the following syntax:

| Cluster   | Type    | Address           |
|-----------|---------|-------------------|
| Dardel    | Primary | dardel.pdc.kth.se |

## Step by step Login tutorial

For step-by-step tutorials on how to login, choose from below the operating system of your local computer
from which you want to access PDC resources. If you face any trouble logging in or need further help, feel free to [Contact Support](../contact/contact_support.md#contact-support).

* [How to login from Linux](linux_login.md)
* [How to login from Windows](windows_login.md)
  * [Install and configure Kerberos and ssh for Windows](windows_login.md#install-and-configure-kerberos-and-ssh-for-windows)
  * [Install and configure Windows Subsystem for Linux (WSL)](windows_login.md#install-and-configure-windows-subsystem-for-linux-wsl)
* [How to login from Mac OS](mac_login.md)
  * [KTH Mac OS X](mac_login.md#kth-mac-os-x)
  * [Own Mac OS X](mac_login.md#own-mac-os-x)
  * [Additional note:](mac_login.md#additional-note)
* [How to reset your Kerberos password](reset_password.md)
  * [Linux, OSX, Windows Subsystem for Linux (WSL)](reset_password.md#linux-osx-windows-subsystem-for-linux-wsl)
  * [Windows](reset_password.md#windows)
* [How to configure kerberos and SSH with kerberos](configuration.md)
  * [Configure Kerberos](configuration.md#configure-kerberos)
  * [Acquire kerberos tickets](configuration.md#acquire-kerberos-tickets)
  * [SSH](configuration.md#ssh)
  * [Firewalls and kerberos](configuration.md#firewalls-and-kerberos)

## Troubleshooting login problems

A lot of solutions for login errors can be found in our FAQ section at [Kerberos](../faq/faq.md#kerberos)
or at [Login](../faq/faq.md#login)

If you do not find a solution, please [Contact Support](../contact/contact_support.md)
with the following information:

* Username
* Which operating system and version you are using
* Any output/error message you got from
  ```default
  kinit -f <username>@NADA.KTH.SE
  ```
* The output from
  ```default
  klist -f
  ```
* The output from
  ```default
  ssh -vvv -o GSSAPIAuthentication=yes <PDC username>@<cluster>.pdc.kth.se
  ```

> [!NOTE]
> If you are using **Conda environments** generation of kerberos tickets via `kinit` will not work. Please, make sure to deactivate your Conda environment before generating tickets.

