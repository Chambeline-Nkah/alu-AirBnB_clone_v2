#!/usr/bin/python3
"""Comment"""
from fabric.api import *
import os
import re
from datetime import datetime

env.user = "ubuntu"
env.hosts = ["3.91.216.134", "54.227.42.244"]
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """Function to compress files in a .tgz archive"""
    try:
        if not os.path.exists("versions"):
            local("mkdir versions")
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Extract archive to /data/web_static/releases/ directory
        archive_filename = os.path.basename(archive_path)
        archive_folder = "/data/web_static/releases/{}".format(
            os.path.splitext(archive_filename)[0]
        )
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))
        run("rm /tmp/{}".format(archive_filename))

        # Move files out of archive folder and remove it
        run("mv {}/web_static/* {}/".format(archive_folder, archive_folder))
        run("rm -rf {}".format(archive_folder + "/web_static"))

        # Delete previous symbolic link and create new one
        run("rm -f /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(archive_folder))
        return True
    except:
        return False
