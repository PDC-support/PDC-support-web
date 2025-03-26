# -*- coding: utf-8 -*-
import subprocess
import shutil
import time
import sys
import re
from pathlib import Path
from datetime import datetime
#-------------------------------------------------------------------------------
def print_help_and_exit():
    script_name = Path(__file__).name
    print("\n*** Usage: python3 update_docs.py\n")
    sys.exit(1)
#-------------------------------------------------------------------------------
def get_command_output(command, exit_after_failure=True):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        if exit_after_failure:
            print("\n*** Error: Non-zero exit code from command '{}'".format(
                " ".join(command)))
            print(e.output.decode("utf-8"))
            sys.exit(1)
        else:
            return ""
    return output.decode("utf-8")
#-------------------------------------------------------------------------------
def check_mkdocs(python_exe):
    print("Checking mkDocs ...")
    get_command_output([python_exe, "-c", "import mkdocs"])
    print("OK\n")
#-------------------------------------------------------------------------------
def check_hugo():
    print("Checking Hugo ...")
    if shutil.which("hugo") is None:
        print("*** Hugo was not found!")
        exit(1)
    print("OK\n")
#-------------------------------------------------------------------------------
def check_git_status():
    print("Checking git status ...")
    output = get_command_output(["git", "status", "--porcelain"])
    if output:
        print("\n*** Error: There are uncommitted changes in the repository.")
        print(output)
        sys.exit(1)
    print("OK\n")
#-------------------------------------------------------------------------------
def check_local_kerberos_ticket():
    print("Checking Kerberos ticket ...")
    ticket_found = False
    kth_username = None
    output = get_command_output(["klist", "-Af"])
    for line in output.splitlines():
        if '@KTH.SE' in line:
            match = re.search(r'[Pp]rincipal:\s+(.*?)@KTH.SE', line)
            if match is not None:
                ticket_found = True
                kth_username = match.group(1)
    if (not ticket_found) or (kth_username is None):
        print("\n*** Error: Could not find Kerberos ticket for KTH.SE.\n")
        sys.exit(1)
    print("{}@KTH.SE\n".format(kth_username))
    return kth_username
#-------------------------------------------------------------------------------
def select_kth_ubuntu_host(kth_username):
    print("Selecting KTH Shell server ...")
    avail_hosts = [
        "staff-shell.sys.kth.se",
        "faculty-shell.sys.kth.se",
    ]
    for kth_ubuntu_host in avail_hosts:
        output = get_command_output(
            ["ssh", "{}@{}".format(kth_username, kth_ubuntu_host), "hostname"],
            exit_after_failure=False)
        time.sleep(0.2)
        if output:
            print(f"{kth_ubuntu_host}\n")
            return kth_ubuntu_host
    else:
        print("\n*** Error: Could not find available KTH Shell server.\n")
        sys.exit(1)
#-------------------------------------------------------------------------------
def check_pdc_admins_membership(kth_username, kth_ubuntu_host):
    print("Checking www-pdc-admins membership ...")
    output = get_command_output([
        "ssh", "{}@{}".format(kth_username, kth_ubuntu_host), "pts", "member",
        "www-pdc-admins"
    ])
    time.sleep(0.2)
    is_member = False
    for line in output.splitlines():
        if kth_username == line.strip():
            is_member = True
    if not is_member:
        print(
            "\n*** Error: User {} is NOT a member of www-pdc-admins\n".format(
                kth_username))
        sys.exit(1)
    print("User {} is a member of www-pdc-admins\n".format(kth_username))
#-------------------------------------------------------------------------------
def check_forwarded_kerberos_ticket(kth_username, kth_ubuntu_host):
    print("Checking forwarded Kerberos ticket ...")
    get_command_output(
        ["ssh", "{}@{}".format(kth_username, kth_ubuntu_host), "klist", "-Af"])
    time.sleep(0.2)
    print("OK\n")
#-------------------------------------------------------------------------------
def make_html():
    print("Making html (may take some time) ...")
    get_command_output(["make", "clean"])
    get_command_output(["make", "build"])
    print("done.\n")
#-------------------------------------------------------------------------------
def upload_html_files(kth_username, kth_ubuntu_host, html_path, afs_path_to_target):
    file_list = [
        str(x) for x in html_path.iterdir() if (x.is_file() or x.is_dir())
    ]
    get_command_output(
        ["scp", "-r"] + file_list +
        ["{}@{}:{}".format(kth_username, kth_ubuntu_host, afs_path_to_target)])
    time.sleep(0.2)
#-------------------------------------------------------------------------------
def move_folder(kth_username, kth_ubuntu_host, html_path, trash_path, exit_after_failure=True):
    get_command_output(
        ["ssh", "{}@{}".format(kth_username, kth_ubuntu_host), "mv", "-f", html_path, trash_path],
        exit_after_failure)
    time.sleep(0.2)
#-------------------------------------------------------------------------------
def copy_folder(kth_username, kth_ubuntu_host, tmp_path, latest_path):
    get_command_output(
        ["ssh", "{}@{}".format(kth_username, kth_ubuntu_host), "cp", "-r", tmp_path, latest_path])
    time.sleep(0.2)
#-------------------------------------------------------------------------------
def delete_folder(kth_username, kth_ubuntu_host, latest_path):
    get_command_output(
        ["ssh", "{}@{}".format(kth_username, kth_ubuntu_host), "rm", "-rf", latest_path])
    time.sleep(0.2)
#-------------------------------------------------------------------------------
def main(gittest, target, html_path):
    print("Copying files from {} to {}".format(html_path, target))

    # Path for source documentation
    html_path = Path(__file__).parent / html_path

    afs_path_to_htdocs = "/afs/kth.se/misc/info/www/pdc.kth.se/htdocs"
    # temporary path for storing newly built pages
    afs_path_to_target_tmp = afs_path_to_htdocs + "/{}-tmp".format(target)

    # permanent path for storing the pages
    afs_path_to_target_latest = afs_path_to_htdocs + "/{}-latest".format(target)

    # temporary path for storing old built pages
    afs_path_to_target_old = afs_path_to_htdocs + "/{}-old".format(target)

    python_exe = sys.executable
    check_mkdocs(python_exe)
    check_hugo()

    kth_username = check_local_kerberos_ticket()
    kth_ubuntu_host = select_kth_ubuntu_host(kth_username)

    check_pdc_admins_membership(kth_username, kth_ubuntu_host)
    check_forwarded_kerberos_ticket(kth_username, kth_ubuntu_host)

    if gittest:
        check_git_status()
    make_html()

    time_string = datetime.now().isoformat(sep='T', timespec='microseconds')
    time_string = time_string.replace('T', '_').replace(':', '-').replace('.', '_')

    print("Uploading html files (may take some time) ...")

    # copy newly built pages to temporary path
    upload_html_files(kth_username, kth_ubuntu_host, html_path, afs_path_to_target_tmp)

    # Move current pages to old
    move_folder(kth_username, kth_ubuntu_host, afs_path_to_target_latest, afs_path_to_target_old, exit_after_failure=False)

    # Move new pages to current
    move_folder(kth_username, kth_ubuntu_host, afs_path_to_target_tmp, afs_path_to_target_latest)

    # Delete old pages
    delete_folder(kth_username, kth_ubuntu_host, afs_path_to_target_old)

    print("done.\n")

    print("{} webpage has been updated at https://support.pdc.kth.se/{}".format(
        target.capitalize(), target))
    print("Please do not forget to push your changes to central repository.")
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    gittest = True
    if len(sys.argv) > 1:
        for idx, arg in enumerate(sys.argv):
            if arg == "-h":
                print("Usage: update_docs...\n")
                print("\n-h")
                print("Help")
                print("\n-g")
                print("Committed git repository is not needed")
                sys.exit(0)
            if arg == "-g":
                gittest = False
    main(gittest, "doc", "site")
#-------------------------------------------------------------------------------
