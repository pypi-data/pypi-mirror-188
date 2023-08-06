#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile
from robin_sd_upload.supportive_scripts import logger

def create_zip(zip_name, folder_name):
    #check if folder exists
    if os.path.isdir(folder_name):
        logger.log(message="Folder exist: " + folder_name, log_level="info", to_file=True, to_terminal=True)
    else:
        return "Folder not exist: " + folder_name
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()