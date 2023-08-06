import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('mylog.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def check_upload_file(upload_file):
    logger.info("Checking upload file...")
    if os.path.isdir(upload_file):
        logger.info("Folder exists: " + upload_file)
        for root, dirs, files in os.walk(upload_file):
            for file in files:
                if file == "Packages.gz" or file == "Packages":
                    logger.info("Packages file found: " + file + " ,assuming this is a valid folder for upload")
                    return True
                else:
                    logger.error("Packages file not found: " + file)
                    return False
    else:
        logger.error("File not valid or not exist: " + upload_file)
        return False
