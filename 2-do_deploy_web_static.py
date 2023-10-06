#!/usr/bin/python3
"""Deploy archive"""
from fabric.api import put, run, local, env
from datetime import datetime
import os
from fabric.decorators import runs_once


env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"
env.hosts = ['54.158.208.45', '3.85.33.151']


@runs_once
def do_pack():
    """packs web_static folder"""

    local("mkdir -p versions")

    dt = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(dt)
    res = local("tar -cvzf {} web_static".format(path))

    if res.failed:
        return None
    return path


def do_deploy(archive_path):
    """ Deploy archive"""

    try:
        if not os.path.exists(archive_path):
            return False

        filename_ext = os.path.basename(archive_path)
        filename = filename_ext[:-4]
        releases_path = "/data/web_static/releases/"

        put(archive_path, "/tmp/{}".format(filename_ext))
        run("rm -rf {}{}".format(releases_path, filename))
        run("mkdir -p {}{}".format(releases_path, filename))
        run("tar -xzf /tmp/{} -C {}{}"
            .format(filename_ext, releases_path, filename))
        run("rm /tmp/{}".format(filename_ext))
        run("mv {0}{1}/web_static/* {0}{1}/".format(releases_path, filename))
        run("rm -rf {}{}/web_static".format(releases_path, filename))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current"
            .format(releases_path, filename))
        print("New version deployed!")
        return True
    except Exception:
        return False
