#!/usr/bin/python3
"""
Fabfile to create and distribute an archive to a web server.
"""

import os.path
from datetime import datetime
from fabric import env
from fabric import local
from fabric import put
from fabric import run

env.hosts = ["54.174.230.101", "100.26.57.164"]


def do_pack():
    """
    Create a tar gzipped archive of the directory web_static.

    Returns:
        str: Path to the created archive file.
             None if the archive creation failed.
    """
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """
    Distribute archive to a web server.

    Args:
        archive_path (str): Path to the archive to be distributed.

    Returns:
        bool: True if the distribution is successful.
            False if the file at the path archive_path doesn't exist
            or if any step of the distribution process fails.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if (
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)
        ).failed
        is True
    ):
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if (
        run(
            "mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(name, name)
        ).failed
        is True
    ):
        return False
    if (
        run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed
        is True
    ):
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if (
        run(
            "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)
        ).failed
        is True
    ):
        return False
    return True


def deploy():
    """
    Create and distribute an archive to a web server.

    Returns:
        bool: True if the deployment is successful.
              False if the archive creation or distribution process fails.
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
