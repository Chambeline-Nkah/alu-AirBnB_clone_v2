#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
import os
from fabric.api import env, put, run

env.hosts = ["3.91.216.134", "54.227.42.244"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    archive_filename = os.path.basename(archive_path)
    archive_no_ext = os.path.splitext(archive_filename)[0]
    tmp_path = "/tmp/{}".format(archive_filename)
    releases_path = "/data/web_static/releases/{}/".format(archive_no_ext)

    try:
        put(archive_path, tmp_path)
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        return True
    except Exception:
        return False
