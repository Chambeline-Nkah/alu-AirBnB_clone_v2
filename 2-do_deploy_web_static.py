#!/usr/bin/python3
"""
    a python script that deploy an archive
"""
from fabric.api import env, run, put
import os


env.hosts = ["3.91.216.134", "54.227.42.244"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.

    Args:
        archive_path: Path to the archive file to be deployed.

    Returns:
        True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]

        # Upload the archive to the /tmp/ directory on the web servers
        put(archive_path, "/tmp/{}".format(archive_name))

        # Uncompress the archive to the appropriate release directory
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                archive_name, archive_no_ext
            )
        )

        # Delete the archive from the web servers
        run("rm /tmp/{}".format(archive_name))

        # Move the contents of the archive to the current release directory
        run(
            "mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(archive_no_ext, archive_no_ext)
        )

        # Remove the empty web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_no_ext))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the deployed release
        run(
            "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(
                archive_no_ext
            )
        )

        return True
    except Exception:
        return False
