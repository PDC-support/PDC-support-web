
# Klemming

## Storage areas

Klemming is divided into three main storage areas shown in the table below. Replace `u/username` by the initial letter of your username and then the full username, and `projectname` by the name of the project. Note that **only the home area is backed up**.

| Area     | Path                                      | Alias         | Size      | File count   | Backup   |
|----------|-------------------------------------------|---------------|-----------|--------------|----------|
| Home     | `/cfs/klemming/home/u/username`           | `$PDC_BACKUP` | 25 GB     | 100 K        | Yes      |
| Projects | `/cfs/klemming/projects/snic/projectname` | -             | Varies    | Varies       | No       |
| Scratch  | `/cfs/klemming/scratch/u/username`        | `$PDC_TMP`    | Unlimited | Unlimited    | No       |

Use the `projinfo` command to show the status of your projects and quotas.

### Home

Use for files that do not belong to a specific project. This area is
considered personal and PDC will not grant access to anyone if not requested by
the owner.  The size is limited to 25 GB and 100,000 files. The data will be
available at least 6 months after the user’s last allocation ended.

### Projects

Used for most non-temporary files that are read and written by jobs running at PDC.
Each project directory belongs to a NAISS storage allocation requested through SUPR,
or to the default storage of a compute allocation.
The amount of data and number of files that can be stored is decided by the active allocation. Once the allocation ends, the project directory can be inherited by
a subsequent allocation by the same PI.

The PI has full access to all data in the project directory.
If the file system permissions do not allow the PI to access requested data, PDC will change those permissions upon request from the PI.
All members should be able to write to the project directory.
It is up to each member, but under the responsibility of the PI, to create suitable subdirectories with the accurate permissions that are needed by the project.

All the data in a project directory will **be deleted 3 months after the project ends**.
The PI will be notified prior of deletion of data through their email address registered in SUPR.

If the space allocated to your project is starting to run out, you should first consider if some files are no longer needed and can be removed. To find out which subdirectories of your project are using the most space run the following command. However, please do not run it more than necessary as it can cause a lot of stress on the file system.

```default
du -sh /cfs/klemming/projects/snic/my_proj/* | sort -hr
```

If you want to see how much space each member of the project is using, run the following command. Note that this can also cause stress on the file system.

```default
find /cfs/klemming/projects/snic/my_proj -printf "%s %u\n" | awk '{arr[$2]+=$1} END {for (i in arr) {print arr[i],i}}' | numfmt --to=iec --suffix=B | sort -hr
```

#### Project groups

The project disk usage is recorded using a separate group per project. These groups are named **pg-<big number>**.
To find the group name of a project directory called **my_proj** you can do:

```default
ls -ld /cfs/klemming/projects/snic/my_proj
```

For files to be accounted to the correct allocation, they all need to belong to that group.
New files should be taken care of automatically by the permissions set on the directory in which they are stored,
i.e. the *set-group-ID bit*. When files are moved from another location, e.g. a users **nobackup** directory or another project’s directory,
the files need to be updated manually with the new group and the user should take responsibility to update the group association directly after the files have been moved.
If you have moved files into a subdirectory called *new_dir* somewhere in the project directory called *my_proj*, changing group association can be done using:

```default
chgrp -hR --reference=/cfs/klemming/projects/snic/my_proj new_dir
find new_dir -type d -exec chmod g+s {} \;
```

The same can also be done simply using the following command:

```default
fixgroup new_dir
```

The system will periodically make sure that all the files in a project directory are associated to the right group and that all the directories
have the set-group-ID bit set. This will not be done often in order to not strain the file system.

### Scratch

Use for temporary files that are read and written by jobs running at PDC.
Examples of this could be files that are only needed during a job or
checkpoint files that become obsolete after the next job starts.

The scratch area is automatically cleaned by removing files that have not been changed in **30** days.

## Performance considerations

Lustre file systems perform quite differently to local disks that are common on other machines.
Lustre was developed for providing fast access to the large data files needed for large parallel applications.
They are particularly bad at dealing with small files and with doing many small operations on these files and those cases should be avoided as much as possible.

### Good practice on a Lustre system

To get the best performance out of a Lustre system you should use as small a number of files as
possible and each time you access a file you should read/write as much data at a time as you can.
An ideal program using Lustre would read in a single data file using parallel IO (e.g. MPI IO),
process the data and then at the end write out a single file again using parallel IO, with no intermediate use of the disk.

If the software is using large files, it can be beneficial to stripe them across several file servers. A common pattern is to use the following command to stripe files in the output directory across as many servers as possible:

```default
lfs setstripe -c -1 output/
```

More information about striping is available on the Lustre wiki: [https://wiki.lustre.org/Configuring_Lustre_File_Striping](https://wiki.lustre.org/Configuring_Lustre_File_Striping).

### Bad practice on a Lustre system

As Lustre is designed for reading a small number of large files quickly, certain IO patterns
that are perfectly fine on other systems cause very high load on a Lustre system e.g.

* Small reads
* Opening many files
* Seeking within a file to read a small piece of data

These practices are very common in applications that were designed to run on systems where each node has its own local scratch disk.
Many software packages (e.g. Quantum Espresso) have input options that reduce the disk IO.

### General best practices

In addition to these guidelines, general storage best practices should be followed:

* Minimize the number of I/O operations, since larger input/output (I/O) operations are more efficient than small ones.
  If possible reads/writes should be aggregated into larger blocks.
* Avoid creating too many files, since post-processing a large number of files can be hard on the file system.
* Avoid creating directories with a large numbers of files. Instead create directory hierarchies, which also improves interactiveness.

### Other things to remember when using Lustre

* Avoid all unnecessary metadata operations – once a file is opened, do as much as possible before closing it again.
  Do not check the existence of files or `stat()` files too often.
* Open files as read-only if possible – read-only files require less locking and therefore put less load on the file system.
* Avoid using `ls` with flags like `-l` , `-F`, or `--color`  as this requires `ls` to `stat()`
  every file to determine its type, which puts an unnecessary load on the file system. Use such flags only
  when the extra information is really needed and do not have them as default.

### After running your processes

* After performing computations at PDC, please move important data files to your own departmental storage system or to a national storage system provided by NAISS (Swestore).
  Remember, space on Lustre is currently limited, and NOT backed up. However, home directories on Dardel (residing in Lustre) are backed up.

## Managing access permissions

By default, only you can access the files in your home and scratch directories, and only project members can access their project directory. But sometimes it is useful to change these defaults.

### Basic Unix permissions

Each file and directory has an owner (user) and a group. The owner can decide whether the owner, members of the group, and others should be able to read (r), write (w) and execute (x) each file. The command `ls -l` displays the permissions for these respectively. For instance `-rw-r-----` means that the owner can read and write to the file, group members can read the file, and others are denied access to the file. The command also shows who is the owner and which is the group. For more details about how to work with file permissions see [this page](https://wiki.archlinux.org/title/File_permissions_and_attributes).


### Access Control Lists

For more advanced use cases, Lustre also supports POSIX ACLs (Access Control Lists). An ACL allows the owner of a file or directory to control access to it on a user-by-user or group-by-group basis. To view and modify an ACL, the commands `getfacl` and `setfacl` are used. Detailed documentation is available by running `setfacl -h` and  `getfacl -h`.

To view the access for a folder in Lustre, run the command:

```default
getfacl -a /cfs/klemming/home/u/user/test
```

You might see output like this:

```default
# file   cfs klemming home u user test
# owner  me
# group  users
user::rwx
group::r-x
other::---
```

Then you can grant the access to another user by

```default
setfacl -m u:<uid>:r-x -R /cfs/klemming/home/u/user/test
```

where `u:<uid>:<permission>` sets the access ACLs for a user. You can specify a user name or UID. The `-R` flag is used for recursively modifying subdirectories with the same permissions. `x` is needed to allow traversal through directories. So for a user to access your subdirectories they need the `x` permission all the way from your top directory (`/cfs/klemming/home/u/user`).

If you want to give another user write permissions replace `r-x` with `rwx`.

Similarly, you can grant the access to another group by

```default
setfacl -m g:<gid>:r-x -R /cfs/klemming/home/u/user/test
```

where `g:<gid>:<permission>` sets the access for a group. You can specify group name or GID.

If you want to give another group write permissions replace `r-x` with `rwx`.

The granted permissions can be removed with the `-x` flag. The following command will remove all permission for another user.

```default
setfacl -x u:<uid> -R /cfs/klemming/home/u/user/test
```

More details about POSIX ACLs can be found on [this page](https://www.usenix.org/legacy/events/usenix03/tech/freenix03/full_papers/gruenbacher/gruenbacher_html/main.html).
