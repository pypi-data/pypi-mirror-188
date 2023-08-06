#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile

from robin_sd_upload.supportive_scripts import logger

# create zip file
def create_zip(file_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zip_file:
        for root, dirs, files in os.walk(file_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path)
    logger.log(message="File added to ZIP: " + file_path, log_level="info", to_file=True, to_terminal=True)
    return zip_name