

# Using rclone to access OneDrive

KTH provides 25 TB of cloud storage to all employees and students through Microsoft OneDrive. The cloud storage can be used for research data not actively in use at PDC, and has options for sharing data between users etc. This page describes how to transfer files between PDC and KTH OneDrive. Other universities may provide similar services.

## Configuring rclone

First rclone must be installed on your local workstation. Instructions are available here: [https://rclone.org/install/](https://rclone.org/install/).

We will use the local client to authenticate with OneDrive, and then copy the configuration file to Dardel.

Start by creating the OneDrive remote:

```default
rclone config create kth_onedrive onedrive
```

This command will open your web browser for you to login. Use `username@ug.kth.se` as the email address.

Now you must set a password to encrypt the configuration file. This step is important since it is not secure to store an unencrypted configuration file on Klemming! Run the following command:

```default
rclone config
```

Press `s` for set password, then `a` to add a new password. Choose a strong password and then press `q` to quit.

Now identify the location of the local configuration file:

```default
rclone config file
```

We must also identify the location of the rclone configuration file on Dardel. Login to Dardel and run the following commands:

```default
ml PDC
ml rclone
rclone config file
```

This should print something like:

```default
Configuration file doesn't exist, but rclone will use this path:
/cfs/klemming/home/x/xyz/.config/rclone/rclone.conf
```

Now we are ready to copy the local file to Dardel. Use the paths collected from the previous commands in place of `LOCAL_PATH` and `REMOTE_PATH`, and run the following on your local workstation:

```default
rsync LOCAL_PATH dardel.pdc.kth.se:REMOTE_PATH
```

!!! WARNING

    Do not copy a configuration file to Dardel if it is not encrypted! Storing an unencrypted configuration file on a shared file system may enable a malicious user to take control over your data.

To test that the setup worked, now run the following on Dardel:

```default
rclone ls kth_onedrive:
```

This command will ask for the password you set earlier and then show a listing of the files you have in OneDrive.

## Transferring files

To transfer files use the `rclone copy` or `rclone sync` commands. For instance, to copy the directory `/cfs/klemming/scratch/x/xyz/results` to OneDrive, use the following command:

```default
rclone copy /cfs/klemming/scratch/x/xyz/results kth_onedrive:
```

To transfer the directory `indata` from OneDrive to Klemming, use the following command:

```default
rclone copy kth_onedrive:indata /cfs/klemming/scratch/x/xyz
```

For larger transfers it is recommended to use the `-P` flag to enable progress indicators in the terminal.

See the rclone usage guide for a complete reference: [https://rclone.org/docs/](https://rclone.org/docs/).

## Limitations

These limitations apply when moving files to OneDrive:

- Up to 25 TB per user
- Max file size 250 GB
- Case insensitive file names
- May throttle bandwidth

If you see excessive throttling, try to using an rclone flag like `--user-agent "ISV|rclone.org|rclone/v1.55.1"`. If this does not work, consider getting your own client id from Microsoft:
[https://rclone.org/onedrive/#getting-your-own-client-id-and-key](https://rclone.org/onedrive/#getting-your-own-client-id-and-key).
