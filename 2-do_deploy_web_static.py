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
    """compress webstatic in a tgz
    the tgz created will be put in folder versions
    """
    if not os.path.exists("versions"):
        local("mkdir versions")
    now = datetime.now()
    name = "versions/web_static_{}.tgz".format(
        now.strftime("%Y%m%d%H%M%S")
    )
    cmd = "tar -cvzf {} {}".format(name, "web_static")
    result = local(cmd)
    if not result.failed:
        return name


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
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, folder_name))

        # Delete the uploaded archive from /tmp/
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the extracted folder to the parent directory
        run("mv {}/web_static/* {}".format(folder_name, folder_name))

        # Remove the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s {} /data/web_static/current".format(folder_name))

        return True
    except Exception as e:
        print(e)
        return False
