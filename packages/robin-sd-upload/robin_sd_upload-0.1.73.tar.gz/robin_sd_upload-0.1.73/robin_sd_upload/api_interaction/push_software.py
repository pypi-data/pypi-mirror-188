#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json

from robin_sd_upload.api_interaction import get_bearer_token
from robin_sd_upload.supportive_scripts import yaml_parser
from robin_sd_upload.supportive_scripts import logger

def push_software(fpath, radarType, version_name):
    config = yaml_parser.parse_config()

    request_url = config['api_url']

    bearer_token = str(get_bearer_token.get_bearer_token())

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }

    # if not bearer_token:
    #     return "Bearer token is empty"
    # else:
    #     print('bearer_token: ', bearer_token)

    # check if can open file path
    if os.path.isfile(fpath):
        logger.log(message="ZIP file exists: " + fpath, log_level="info", to_file=True, to_terminal=True)
        # print("ZIP file exists: " + fpath)
    else:
        logger.log(message="ZIP not exist: " + fpath, log_level="error", to_file=True, to_terminal=True)
        # print("ZIP not exist: " + fpath)
        return "ZIP not exist: " + fpath
        
    files = {
        'file': (fpath, open(fpath, 'rb'))
    }

    values = {
        'destination': json.dumps(radarType),
        'versionName': json.dumps(version_name)
    }
    
    # print versionName
    # print('versionName: ', version_name)
    # print('values.versionName: ', values['versionName'])

    logger.log(message="Pushing software to Robin SD", log_level="info", to_file=True, to_terminal=True)

    response = requests.post(request_url + '/api/softwares/softwarefiles', headers=headers, data=values, files=files)
    return response.json()