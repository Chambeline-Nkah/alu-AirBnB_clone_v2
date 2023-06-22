#!/usr/bin/python3
"""Write a Fabric script that generates a .tgz
archive from the contents of the web_static folder"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """do_pack fxn"""
    local("mkdir -p versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.failed:
        return None
    else:
        return archive_path
