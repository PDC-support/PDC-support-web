
# File transfer

!!! note

    All examples below are created if you want to transfer small amount of data in/out of *klemming*
    In case you would like to transfer a large amount of data, please use the transfer node instead
    `dardel-ftn01.pdc.kth.se/`

## Using rsync

### Using rsync from Ubuntu Linux 

rsync copies files between hosts on a network.
It uses SSH for data transfer, and uses the same authentication and provides the same security as `ssh`. Before using `rsync`,
make sure you have a working SSH setup on your local machine.
More information on `rsync` at https://linux.die.net/man/1/rsync

#### Transferring from your local machine to PDC

Standing in a directory on your local computer containing the file `localfile`.

```default
rsync <localfile> <username>@dardel.pdc.kth.se:<path>
```

where `username` is your username at PDC and `path` is the path on klemming. You can copy it to the `Private`
directory on your PDC home directory using `~`. Example: ~/Private/ or /cfs/klemming/projects/supr/<projectname>
For more information about what nodes to use see [Nodes for file operations](data_management.md#nodes-for-file-operations)

!!! note

    Do not use `rsync -a`
    When transferring directly to a project directory or the scratch area, please do not use the `-a` flag of the `rsync` command. Doing so will incorrectly set the group of the transferred files so that they will be accounted to you personal quota, rather than the project/scratch quota. 

!!! note

    In most cases it is sufficient to use `rsync -r` to transfer a directory.

#### Transferring from PDC to your local machine

Standing in a directory on your local computer whereto you want to copy the file pdcfile from
`/cfs/klemming/home/<1st letter username>/<username>/` you can transfer it using the command:

```default
rsync <username>@dardel.pdc.kth.se:/cfs/klemming/scratch/<1st letter username>/<username>/<pdcfile> .
```

where `username` is your username at PDC.

!!! note 

    If your `.bashrc` or other shell configuration files produce **ANY** output, then `scp` can fail.
    You can test this with the command below. If the command produces output,
    then you need to fix your shell configuration files so that they do not produce output.

    ```default
    ssh <username>@dardel.pdc.kth.se /bin/true
    ```

For more information about what nodes to use see [Nodes for file operations](data_management.md#nodes-for-file-operations)

### Interrupted transfer

The benefit of user ´rsync´ is that the command has added functionality in case of interrupted transfers.
The following command resumes transfer by appending only missing data and see to it that incomplete files are kept.

```default
rsync --partial --append-verify <localfile> <username>@dardel.pdc.kth.se:<path>
```

## Using scp

### Using scp from Ubuntu Linux 

SCP: (secure copy) copies files between hosts on a network.
It uses SSH for data transfer, and uses the same authentication and provides the same security as `ssh`. Before using `scp`,
make sure you have a working SSH setup on your local machine.

#### Transferring from your local machine to PDC

Standing in a directory on your local computer containing the file `localfile`.

```default
scp <localfile> <username>@dardel.pdc.kth.se:<path>
```

where `username` is your username at PDC and `path` is the path on klemming. You can copy it to the `Private`
directory on your PDC home directory using `~`. Example: ~/Private/ or /cfs/klemming/projects/supr/<projectname>
For more information about what nodes to use see [Nodes for file operations](data_management.md#nodes-for-file-operations)

!!! note

    In most cases it is sufficient to use `scp -r` to transfer a directory.

#### Transferring from PDC to your local machine

Standing in a directory on your local computer whereto you want to copy the file pdcfile from
`/cfs/klemming/home/<1st letter username>/<username>/` you can transfer it using the command:

```default
scp <username>@dardel.pdc.kth.se:/cfs/klemming/scratch/<1st letter username>/<username>/<pdcfile> .
```

where `username` is your username at PDC.

!!! note 

    If your `.bashrc` or other shell configuration files produce **ANY** output, then `scp` can fail.
    You can test this with the command below. If the command produces output,
    then you need to fix your shell configuration files so that they do not produce output.

    ```default
    ssh <username>@dardel.pdc.kth.se /bin/true
    ```

For more information about what nodes to use see [Nodes for file operations](data_management.md#nodes-for-file-operations)


### Using scp psftp from Windows

If you’re using *PuTTY* to login to PDC clusters, you can use **PSFTP** or **PSCP** that follows the PuTTY installation.
To use **PSCP**, you need a saved session which is used for login on Dardel. As an example, save the session with the name *dardel* for dardel.pdc.kth.se

#### Using pscp

To use PSCP, open up the command prompt, i.e run cmd. Use PSCP to transfer the files using the
Saved Session you previously added in PuTTY.
The syntax is similar to scp (i.e. -r for recursive etc).

To transfer a file from your local computer to Lustre (if you have saved the file transfer session in PuTTY as *dardel*)

```default
"C:\Program Files\PuTTY\pscp.exe" -load dardel C:\<file to transfer> <username>@dardel.pdc.kth.se:/cfs/klemming/home/<1st letter username>/<username>
```

#### Using psftp

To start PSFTP navigate to the folder PuTTY is installed and double click on psftp.exe, or search for *PSFTP* on the Windows main menu. Note that just like PuTTY, you need a kerberos ticket to use PSFTP.

If you have multiple sessions in PuTTY clicking the PSFTP executable might load the wrong settings. If that happens you have to start PSFTP from the command prompt with an argument specifying the session you created for our cluster
(e.g. *dardel*, see above).

```default
"C:\Program Files\PuTTY\psftp.exe" -load dardel
```

When you have started PSFTP, a new terminal will open. Here, you first have to connect to the cluster. You can do this by typing

```default
open <username>@dardel.pdc.kth.se
```

If you have followed the step from [Windows Login](../login/windows_login.md)
and saved a login session (example: dardel) you can also type \`\` open filetransfer\`\` instead. At the psftp> prompt you can then use the standard
ftp commands (cd, lcd, get, put, …).

Now you have logged in to the cluster and you’re in your *AFS Home Directory*.
You can change your **remote** directory location to your cfs directory with

```default
cd /cfs/klemming/home/<1st letter username>/<username>/<folder>
```

You can also change your **local** directory location with

```default
lcd c:<1st letter username>/<username>/<file folder>
```

Keep in mind that the location should be specified in the same way you change directory on a Windows terminal, for `lcd`.

You can transfer files by using **get** or **put**. *get* will transfer files specified from remote location to current local directory,
and *put* will transfer files from current local directory to the current remote directory.

```default
get <filename>
```

For more information about PSFTP utility and commands, please look at [http://the.earth.li/~sgtatham/putty/0.63/htmldoc/](http://the.earth.li/~sgtatham/putty/0.63/htmldoc/)

### Using scp rsync from Mac OS

`scp` and `rsync` work the same on Mac OS as they do on Linux, see information at [Using scp/rsync from Ubuntu (Linux)](#using-scp-rsync-from-ubuntu-linux)
