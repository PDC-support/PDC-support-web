

# How to reset your Kerberos password

This section describes how to reset your kerberos password
in different operating systems, if you remember your current password.

## Linux OSX Windows Subsystem for Linux WSL 

Changing your kerberos password is straightforward by using **kpasswd**

* Open your favorite *shell*
* ```default
  $ kpasswd [username]@NADA.KTH.SE
  [username]@NADA.KTH.SE's Password:
  New password for [username]@NADA.KTH.SE:
  Retype New password for [username]@NADA.KTH.SE:
  ```

## Windows

If you are not using *Windows Subsystem for Linux (WSL)* you must
instead use the graphical Network Identify Manager

1. **Open Network Identity Manager (NIM)**
1. Select your *kerberos credential*
1. Select menu item **Credential** -> **Change password**
1. Check that the top part of the window verifies your [username]@NADA.KTH.SE
1. Enter current and new password
1. Press **Finish**
