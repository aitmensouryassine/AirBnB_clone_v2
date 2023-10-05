#!/usr/bin/python3
"""
Module to compress data before sending
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """packs web_static folder"""

    local("mkdir -p versions")

    path = "versions/web_static_{}.tgz"\
        .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
    res = local("tar -cvzf {} web_static".format(path))

    if res.failed:
        return None
    return path
