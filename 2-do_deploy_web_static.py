#!/usr/bin/python3
"""
Writing a Fabric script that distributes
an archive to my web servers
"""
import os
from fabric.api import put, run, env
env.hosts = ['34.224.26.174', '18.208.221.76']


def do_deploy(archive_path):
    """
    do_deploy fxn
    """
    if archive_path is None or not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        file_name = file.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, "/tmp/")

        run("mkdir -p {}{}/".format(path, file_name))

        run("tar -xzf /tmp/{} -C {}{}/".format(
            file, path, file_name))

        run("rm /tmp/{}".format(file))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, file_name))

        run("rm -rf {}{}/web_static".format(path, file_name))
        run("rm -rf /data/web_static/current")

        run("ln -s {}{}/ /data/web_static/current".
            format(path, file_name))
        return True
    except BaseException:
        return False
