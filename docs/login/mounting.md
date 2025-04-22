
# How to mount a Dardel directory on your local computer

`sshfs` is a userspace filesystem which mounts a remote directory in the local filesystem using the ssh protocol.

## sshfs on Linux

### Installing sshfs

To install `sshfs` using apt-get, do

```default
sudo apt-get install sshfs
```

### Using sshfs

Assume that Anna with Dardel user name anna wants to mount her Dardel
scratch directory on her local Linux machine. She would then:

1. Obtain kerberos tickets as described [here](kerberos_login.md).
2. Create a local directory using
```
mkdir dardel-scratch
```

3. Mount the Dardel scratch directory using
```
sshfs anna@dardel.pdc.kth.se:/cfs/klemming/scratch/a/anna dardel-scratch
```

The dardel-scratch directory can then be used as if it was local.

### Unmounting an sshfs directory

It is good practise to explicitly unmount the remote directory when
finished. Strange things may happen if network connectivity is lost.

To unmount the directory in the Anna example above, do

```
fusermount -zu dardel-scratch
```
