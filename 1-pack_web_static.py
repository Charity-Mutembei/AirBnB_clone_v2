#!/usr/bin/python3
"""Put everything in the web static
"""
from fabric.api import local
from datetime import datetime
import os


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
