#!/usr/bin/python3
"""
Fabric script : deletes out-of-date archives
"""
from fabric.api import put, run, local, env, lcd, cd
from fabric.decorators import runs_once
from datetime import datetime
import os


env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"
env.hosts = ['54.158.208.45', '3.85.33.151']


@runs_once
def do_pack():
    """packs web_static folder"""

    local("mkdir -p versions")

    path = "versions/web_static_{}.tgz"\
        .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
    res = local("tar -cvzf {} web_static".format(path))

    if res.failed:
        return None
    return path


def do_deploy(archive_path):
    """ Deploy archive"""

    if not os.path.exists(archive_path):
        return False

    try:
        filename_ext = os.path.basename(archive_path)
        ext_length = ".tgz".length
        filename = filename_ext[:-ext_length]

        put(archive_path, "/tmp/{}".format(filename_ext))
        run("rm -rf /data/web_static/releases/{}".format(filename))
        run("mkdir -p /data/web_static/releases/{}".format(filename))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(filename_ext, filename))
        run("rm /tmp/{}".format(filename_ext))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(filename, filename))
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Deploy"""

    filepath = do_pack()

    if filepath is None:
        return False
    return do_deploy(filepath)


def do_clean(number=0):
    """Deletes a giver number of archives"""

    num = int(number)
    if num == 0:
        num == 1

    with lcd("versions"):
        local("ls -dt * | tail -n +{} | sudo xargs rm -f".format(num))

    with cd("/data/web_static/releases"):
        run("ls -dt * | tail -n +{} | sudo xargs rm -rf".format(num))
