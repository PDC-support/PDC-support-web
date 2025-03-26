
# Swestore

## Some important consideration before using Swestore

### Introduction

Swestore-dCache is distributed storage infrastructure. Data is stored in two copies with each copy at a different NAISS centre.
To protect against silent data corruption the dCache storage system checksums all stored data and periodically verifies the data using this checksum.
The dCache system does NOT yet provide protection against user errors like inadvertent file deletions.

For more information, see [NAISS Swestore documentation](https://docs.swestore.se/)

### Requirements

To access Swestore-dCache, using rclone, you need to be a member of a Swestore storage project, see Getting access to Swestore.
Depending on your preference and security needs, you can use rclone with either certificate or username/password authentication.
We will focus on username/password in this guide.

## Swestore dCache access from PDC transfer node

1. Login to one of the transfer nodes
   ```text
   # get a 7 days forwardable ticket
   $ kinit --forwardable -l 7d <user>@NADA.KTH.SE

   #login to transfer node
   $ ssh <user>@dardel.pdc.kth.se
   ```

   Note: Please consider time required for files to transfer, and kerberos default ticket lifetime. You can request up to 30-days forwardable kerberos ticket. Considering that it might take time to do file transfers, we suggest to do it from screen or tmux. In order to keep your access to the AFS filesystem in screen  after logging out from your original ssh session you need to have started the original screen like following:
   ```text
   # $ pagsh bash  c "export KRB5CCNAME=$KRB5CCNAME; afslog; screen  S transfer"
   ```
1. Load the PDC and rclone module
   ```text
   $ ml PDC rclone
   ```
1. Configure rclone to connect to Swestore-dCache
   ```text
     # start configuration of “new remote”
     $ rclone config
       No remotes found - make a new one
       n) New remote
       s) Set configuration password
       q) Quit config
       n/s/q> n

     # give name to “new remote”
       name> swestore

     # chose webdav as type  i e  40 
       Option Storage.
       Type of storage to configure.
       Enter a string value. Press Enter for the default ("").
       Choose a number from below, or type in your own value.
       1 / 1Fichier
         \ "fichier"
       2 / Alias for an existing remote
         \ "alias"
       3 / Amazon Drive
         \ "amazon cloud drive"
         ………(etc)………
       39 / Uptobox
         \ "uptobox"
       40 / Webdav
         \ "webdav"
       41 / Yandex Disk
         \ "yandex"
       42 / Zoho
         \ "zoho"
       43 / http Connection
         \ "http"
       44 / premiumize.me
         \ "premiumizeme"
       45 / seafile
         \ "seafile"
       Storage> 40

     # provide Swestore webdav endpoint   https   webdav swestore se
       Option url.
       URL of http host to connect to.
       E.g. https://example.com.
       Enter a string value. Press Enter for the default ("").
       url> https://webdav.swestore.se

     # choose “other” as vendor option
       Option vendor.
       Name of the Webdav site/service/software you are using.
       Enter a string value. Press Enter for the default ("").
       Choose a number from below, or type in your own value.
       1 / Nextcloud
         \ "nextcloud"
       2 / Owncloud
         \ "owncloud"
       3 / Sharepoint Online, authenticated by Microsoft account
         \ "sharepoint"
       4 / Sharepoint with NTLM authentication, usually self-hosted on-premises
         \ "sharepoint-ntlm"
       5 / Other site/service or software
         \ "other"
       vendor> 5

     # provide your Swestore username
       Option user.
       User name.
       In case NTLM authentication is used, the username should be in the format 'Domain\User'.
       Enter a string value. Press Enter for the default ("").
       user> s_dejvi

     # provide your Swestore password
       Option pass.
       Password.
       Choose an alternative below. Press Enter for the default (n).
       y) Yes type in my own password
       g) Generate random password
       n) No leave this optional password blank (default)
       y/g/n> y
       Enter the password:
       Password: *****************
       Confirm the password:
       Password: *****************

     # choose NO as bearer token
       Option bearer_token.
       Bearer token instead of user/pass (e.g. a Macaroon).
       Enter a string value. Press Enter for the default ("").
       bearer_token>
       Edit advanced config?
       y) Yes
       n) No (default)
       y/n> n
   --------------------
   [swestore]
   type = webdav
   url = https://webdav.swestore.se
   vendor = other
   user = s_dejvi
   pass = *** ENCRYPTED ***
   --------------------
     y) Yes this is OK (default)
     e) Edit this remote
     d) Delete this remote
     y/e/d> y
   Current remotes:

   Name Type
   ==== ====
   swestore webdav

   e) Edit existing remote
   n) New remote
   d) Delete remote
   r) Rename remote
   c) Copy remote
   s) Set configuration password
   q) Quit config
   e/n/d/r/c/s/q> q
   ```
1. And now you can use rclone to transfer/manage files on the system. You can test it, with ‘rclone lsd’ command, by listing directories:
   ```text
   $ rclone lsd swestore:/snic/
   ```

### Basic rclone commands

Run “rclone” to list available commands and “rclone command –help” to see the help for that command.
You can also find more information about rclone commands here [https://rclone.org/commands/](https://rclone.org/commands/) or on NAISS Swestore-dCache documentation
[https://docs.swestore.se/](https://docs.swestore.se/)

## Security considerations when using rclone

Your rclone configuration file, generated by interactive configuration session, is stored in your home directory.

```text
$ rclone config file
Configuration file is stored at:
/cfs/klemming/home/v/vitlacil/.config/rclone/rclone.conf
```

Important The crypt password stored in rclone.conf is lightly obscured. That only protects it from cursory inspection. It is not secure unless configuration encryption of rclone.conf is specified.

More information on configuration encryption is available here [https://rclone.org/docs/#configuration-encryption](https://rclone.org/docs/#configuration-encryption)
