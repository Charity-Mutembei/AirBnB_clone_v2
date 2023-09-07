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
        Distribute archive.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False

def deploy():
    """
    Deploy the archive to the web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
