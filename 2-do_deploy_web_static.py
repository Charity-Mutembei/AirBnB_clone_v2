#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run, prompt
import os

# Prompt for the list of hostnames (comma-separated) and the username
hostnames = prompt("Enter a comma to separate (e.g., host1,host2): ")
username = prompt("Enter the username: ")

# Set the list of hosts and the username in the env dictionary
env.hosts = [hostname.strip() for hostname in hostnames.split(",")]
env.user = username


def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the base name of the archive
        archive_name = os.path.basename(archive_path)

        # Define the remote paths
        remote_tmp_path = "/tmp/"
        remote_archive_path = remote_tmp_path + archive_name
        remote_release_path = "/data/web_static/releases/"
        archive_folder_name = archive_name[:-4]

        # Upload the archive to the /tmp/ directory of the web servers
        put(archive_path, remote_tmp_path)

        # Create the directory for the new version
        run("mkdir -p {}{}/".format(remote_release_path, archive_folder_name))

        # Uncompress the archive to the folder on the web servers
        run("tar -xzf {}{} -C {}{}/".format
            (
                remote_tmp_path,
                archive_name,
                remote_release_path,
                archive_folder_name
                ))

        # Delete the archive from the web servers
        run("rm -f {}{}".format(remote_tmp_path, archive_name))

        # Delete the current symbolic link
        run("rm -f /data/web_static/current")

        # Create a new symbolic link linked to the new version
        run("ln -s {}{}/ /data/web_static/current".format(
            remote_release_path,
            archive_folder_name
            ))

        return True

    except Exception:
        return False
