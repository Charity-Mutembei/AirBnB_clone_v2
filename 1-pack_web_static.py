#!/usr/bin/python3
"""Put everything in the web static
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.
    """
    try:
        # Create the versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Get the current date and time
        now = datetime.now()

        # Format the date and time as a string
        date_time_str = now.strftime("%Y%m%d%H%M%S")

        # Create the archive filename
        archive_name = "web_static_{}.tgz".format(date_time_str)

        # Compress the web_static folder into the archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the archive path if successful
        return "versions/{}".format(archive_name)
    except Exception:
        return None
