

# How to configure kerberos and SSH with kerberos

This section describes how to configure kerberos.

## Configure Kerberos

You need to configure **Kerberos** so we are able to find the PDC domain.

The configuration file for kerberos on **linux** and **OSX** that you need to edit is **/etc/krb5.conf** as root.
If you are not able to become root on your machine, you can create a file in your home
directory called for example **~/pdckrb**.
After this, you need to set the path for kerberos like

```text
# For bash
export KRB5_CONFIG=~/pdckrb/krb5.conf
# For tcsh
setenv KRB5_CONFIG  ~/pdckrb/krb5.conf
```

For **Windows**, the kerberos file should be located at

```text
C:\ProgramData\krb5.conf
```

or

```text
C:\ProgramData\Kerberos\krb5.conf
```

**krb5.conf** should be defined with the following entries

```text
[domain_realm]
  .pdc.kth.se = NADA.KTH.SE

[appdefaults]
  forwardable = yes
  forward = yes
  krb4_get_tickets = no

[libdefaults]
  default_realm = NADA.KTH.SE
  dns_lookup_realm = true
  dns_lookup_kdc = true
```


## Acquire kerberos tickets

In order to get a kerberos ticket, you first need to startup your command shell.
On Windows, search for **cmd**.

To acquire tickets…

```text
kinit -f <PDC username>@NADA.KTH.SE
```

You will be asked for your PDC password and then you have acquired your ticket.

On Windows it is important that you run the correct version of the software, since
several version can be installed by default Windows.
Execute…

```text
where kinit
c:\windows\system32\kinit.exe
c:\program files\heimdal\bin\kinit.exe
```

…to find out which executable you are running. The heimdal kerberos
in the *program files* folder or where you have installed it. In order to execute
the heimdal version you have to enter the complete path.

```text
c:\"program files"\heimdal\bin\kinit.exe
```

You can see what active tickets you have using

```text
klist -f
```

Even regarding this command, it is important that you do run the
heimdal kerberos and should define the right path. (See instructions above)

```text
where klist
c:\windows\system32\klist.exe
c:\program files\heimdal\bin\klist.exe
```

More information about kerberos can be found at [http://web.mit.edu/kerberos/krb5-current/doc/user/index.html](http://web.mit.edu/kerberos/krb5-current/doc/user/index.html)


## SSH

This section describes how to configure SSH using Kerberos.
This procedure does work only for **Linux** and **Mac**.
For Windows, please read information at [Setting up PuTTY](windows_login.md#how-to-login-from-windows)

### SSH without configuration

In order to login you need to supply these options directly to the ssh command.

```text
ssh -o GSSAPIAuthentication=yes <username>@<cluster>.pdc.kth.se
```

### SSH with configuration

**These are instructions on the configuration file for use of SSH with Kerberos.
If you are using SSH with an SSH key pair, please refer to the page** [How to log in with SSH keys](ssh_login.md#how-to-log-in-with-ssh-keys)

OpenSSH can be configured with command line arguments or a configuration file
to simplify the login procedure.
The options in the configuration file are parsed in order.
Create or modify the file **~/.ssh/config**

```text
# Hosts we want to authenticate to with Kerberos
Host *.kth.se *.kth.se.
# User authentication based on GSSAPI is allowed
GSSAPIAuthentication yes
# Hosts to which we want to delegate credentials  Try to limit this to
# hosts you trust  and where you really have use for forwarded tickets 
Host *.csc.kth.se *.csc.kth.se. *.nada.kth.se *.nada.kth.se. *.pdc.kth.se *.pdc.kth.se.
# All other hosts
Host *
```

The file should be named **config**, and if this is not the case, please
rename it.

Do remember to set the right permission on the file

```text
chmod 644 ~/.ssh/config
```

After this, you can log in by using

```text
ssh <username>@<cluster>.pdc.kth.se
```


## Firewalls and kerberos

When a firewall is installed between your workstation and the computers at PDC, a special configurations described below may be necessary to use Kerberos.

1. Ports used by Kerberos. Contact your system administrators and make sure that a firewall is really the problem. Kerberos uses in its standard configuration the following ports for communication:

   | Port name                   |   Port number | Port type   | Comment                                                                 |
   |-----------------------------|---------------|-------------|-------------------------------------------------------------------------|
   | kerberos                    |            88 | UDP         | Default configuration                                                   |
   | kerberos                    |            88 | TCP         | Alternative configurations<br/>for usage with firewalls<br/>(see below) |
   | http<br/>(used by kerberos) |            80 | TCP         |                                                                         |
   | ssh                         |            22 | TCP         | Usually already open                                                    |
   | ftp-data                    |            20 | TCP         |                                                                         |
   | ftp                         |            21 | TCP         |                                                                         |
   | kpasswd                     |           464 | UDP         | Only for password change                                                |

  If possible, open UDP port 88 for bidirectional communication. This is the default (and preferred) mode of operation. Otherwise continue with the next step. After that, try to contact our authentication server with kinit as described before.
1. If there is no contact through UDP port 88, open TCP port 88 for outgoing traffic instead (if possible), and try kinit again. If it still does not work, continue with the next step.
1. The next thing to try is to get Kerberos to communicate via http over TCP port 80. This port is often open, since it is needed for surfing the web.
   1. Create the Kerberos configuration file. In addition you need to add the following
      ```text
            [realms]
      NADA.KTH.SE = {
              kdc = kerberos.nada.kth.se
              kdc = http/kerberos.nada.kth.se
              kdc = kerberos-1.nada.kth.se
              kdc = http/kerberos-1.nada.kth.se
              kdc = kerberos-2.nada.kth.se
              kdc = http/kerberos-2.nada.kth.se
              admin_server = kerberos.nada.kth.se
              }
      ```

      If kinit <username>@NADA.KTH.SE succeeds but ssh <username>@hostname does not, then you
      might want to have a look at your crendential cache with klist. If it does not contain any
      rows that look like host/<something>@NADA.KTH.SE, you need to get host credentials manually.
      That can be done with the following command for a host named hostname:
      ```text
      $ host hostname | awk '$3 == "address" {print "host "$4}' | bash \
      | awk '{sub(".$",""); print "kgetcred host/"$NF"@NADA.KTH.SE"}' | bash
      ```

      If hostname is dardel.pdc.kth.se, after that, the output from klist should contain something like
      ```text
      Apr 14 16:33:11 2015  Apr 16 10:26:05 2015  host/dardel-login2.pdc.kth.se@NADA.KTH.SE
      ```
   1. In some systems, all http communication (i.e. web traffic) must go through a proxy.
      If that is the case, you can probably find out it’s address by looking at the settings of your web
      browser. If not, ask your system administrator.

      To instruct kerberos to go through the proxy, add the following line to the [libdefaults]
      section of krb5.conf:
      ```text
      http_proxy = http://address.of.proxy:port
      ```
