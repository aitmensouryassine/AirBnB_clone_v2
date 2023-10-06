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

    filename_ext = os.path.basename(archive_path)
    filename = filename_ext[:-4]

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}".format(filename))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(filename_ext, filename))
        run("rm /tmp/{}".format(filename_ext))
        run("mv /data/web_static/releases/{}/web_static/*"
            " /data/web_static/releases/{}/".format(filename, filename))
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
    except Exception:
        return False

    print("New version deployed!")
    return True


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

    versions = os.listdir("versions")
    versions = sorted(versions)

    for i in range(num):
        versions.pop()

    with lcd("versions"):
        for filename_ext in versions:
            local("rm -rf ./{}".format(filename_ext))

    with cd("/data/web_static/releases"):
        releases = run("ls -tr").split()
        web_static_list = [release for release in releases
                      if "web_static_" in release]

        for i in range(num):
            web_static_list.pop()

        for web_static in web_static_list:
            run("rm -rf ./{}".format(web_static))
