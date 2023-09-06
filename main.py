###################################
# Version: v1                     #
###################################
# Developer: Zero Industries      #
# Software: AutoCoC               #
###################################
# DO NOT COPY WIHTOUT PERMISSION! #
###################################

from zero_industries_devpackage.logger import Logger
from zero_industries_devpackage.zeropi import ZeroApi

class AutoCoC:

    def __init__(self):
        pass


if __name__ == "__main__":
    api = ZeroApi("autococ", "v2", True)
    logger = Logger("main")

    if api.is_available():
        logger.write("Api reachable... Starting")
        if not api.get_version():
            logger.write("No version could be requested...")

    else:
        logger.write("Failed to fetch api! Stopping service", "fail")