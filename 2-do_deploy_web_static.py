#!/usr/bin/python3
"""compress and send to server
"""
from fabric.api import local, env, run, put
from datetime import datetime
import os
env.hosts = ['35.231.156.161', '34.73.64.44']
env.user = 'ubuntu'


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
    """send archive to server
    Arguments:
        archive_path: the archive tgz file to send
    """
    if not archive_path or not os.path.exists(archive_path):
        return False
    put(archive_path, '/tmp')
    ar_name = archive_path[archive_path.find("/") + 1: -4]
    try:
        run('mkdir -p /data/web_static/releases/{}/'.format(ar_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(
                ar_name, ar_name
        ))
        run('rm /tmp/{}.tgz'.format(ar_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(
                ar_name, ar_name
        ))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            ar_name
        ))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(
            ar_name
        ))
        print("New version deployed!")
        return True
    except:
        return False
