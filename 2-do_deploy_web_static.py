#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run, local
from datetime import datetime
import os

env.hosts = ["100.25.180.249", "54.196.30.13"]
env.user = "ubuntu"

def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.
    """
    try:
        # Create the versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Get the current date and time
        now = datetime.now()

        # Format the date and time as a string
        date_time_str = now.strftime("%Y%m%d%H%M%S")

        # Create the archive filename
        archive_name = "web_static_{}.tgz".format(date_time_str)

        # Compress the web_static folder into the archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the archive path if successful
        return "versions/{}".format(archive_name)
    except Exception:
        return None

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
        run("tar -xzf {}{} -C {}{}/".format(remote_tmp_path, archive_name, remote_release_path, archive_folder_name))

        # Delete the archive from the web servers
        run("rm -f {}{}".format(remote_tmp_path, archive_name))

        # Delete the current symbolic link
        run("rm -f /data/web_static/current")

        # Create a new symbolic link linked to the new version
        run("ln -s {}{}/ /data/web_static/current".format(remote_release_path, archive_folder_name))

        return True

    except Exception:
        return False
