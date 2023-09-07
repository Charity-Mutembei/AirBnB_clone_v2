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
    """Distribute an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the web_static/releases/ directory
        archive_filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(
            archive_filename[:-4])
        run("sudo mkdir -p {}".format(folder_name))
        run(" sudo tar -xzf /tmp/{} -C {}".format(
            archive_filename, folder_name))

        # Delete the uploaded archive from /tmp/
        run(" sudo rm /tmp/{}".format(archive_filename))

        # Move the contents of the extracted folder to the parent directory
        run("sudo mv {}/web_static/* {}".format(folder_name, folder_name))

        # Remove the symbolic link /data/web_static/current
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("sudo ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Deploy the archive to the web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
