

# How to login from Mac OS

This section describes how to acquire Kerberos tickets and log in from different versions of Mac OS X.

For information on how to login from linux using SSH key based authentication, please refer to [this page](./ssh_login.md#linux-and-macos)

## KTH Mac OS X

In case you are using a Mac computer installed by KTH, everything
should be installed.
In case of any problems please contact [it-support@kth.se](mailto:it-support@kth.se)

Otherwise follow instructions below.

## Own Mac OS X

First get Kerberos tickets using default `kinit` (full path `/usr/bin/kinit`):

```default
kinit your-username@NADA.KTH.SE
```

Check that valid tickets exist:

```default
klist -f
```

You should get a similar output as the following one:

```text
Credentials cache: API:0E4B40BC-F22B-43B8-87E2-BA13538CF042
      Principal: your-username@NADA.KTH.SE

      Issued                Expires               Principal
      Aug 27 08:28:40 2023  Aug 27 18:28:37 2023  krbtgt/NADA.KTH.SE@NADA.KTH.SE
```

!!! note

      Using the full path of Kerberos binaries, i.e. `usr/bin/kinit` instead of `kinit` for example, is particularly important if you have an active conda environment in your local computer's shell.

Now you are good to go:

```default
ssh -o GSSAPIAuthentication=yes  your-username@dardel.pdc.kth.se
```

In this case, dardel prompt should appear:

```default
dardel-login-1:~$
```

Check that tickets have been forwarded:

```default
dardel-login-1:~$ klist
```

The output should be similar to this:

```text
Credentials cache: FILE:/tmp/krb5cc_18118_oZ0CMh5rsk
      Principal: your-username@NADA.KTH.SE

      Issued                Expires               Principal
      Aug 27 08:30:05 2020  Aug 27 18:28:37 2023  krbtgt/NADA.KTH.SE@NADA.KTH.SE
      Aug 27 08:30:05 2020  Aug 27 18:28:37 2023  afs/pdc.kth.se@NADA.KTH.SE
```

Notice these are the tickets in the `FILE:` cache in Dardel.

Other useful commands to check the state of your tickets are `klist -l`, which shows all caches, and `klist -v`, which shows more detailed information on the acquired tickets.

## Additional note 

In order to login you need to supply the option directly to the ssh command.

```default
ssh -o GSSAPIAuthentication=yes your-username@dardel.pdc.kth.se
```

OpenSSH can be configured with command line arguments or a configuration file to simplify the login procedure. The options in the configuration file are parsed in order. Create or modify the file **~/.ssh/config**

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

Do remember to set the right permission on the file

```default
chmod 644 ~/.ssh/config
```

After this, you can log in by using

```default
ssh your-username@dardel.pdc.kth.se
```
