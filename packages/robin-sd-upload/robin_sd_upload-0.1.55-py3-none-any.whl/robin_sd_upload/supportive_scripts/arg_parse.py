#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import argparse
import yaml

# from ..validate import validate
# from ..create_zip import create_zip
# from ..api_interaction.push_software import push_software
# from ..remove_zip import remove_zip
# from ..parse_config import parse_config
# from ..check_upload_file import check_upload_file

from robin_sd_upload.api_interaction import push_software
from robin_sd_upload import _version
from robin_sd_upload.slack_interaction import slack_handler
from robin_sd_upload.supportive_scripts import yaml_parser
from robin_sd_upload.supportive_scripts import logger
from robin_sd_upload.supportive_scripts import validate
from robin_sd_upload.supportive_scripts import create_zip
from robin_sd_upload.supportive_scripts import remove_zip
from robin_sd_upload.supportive_scripts import parse_config_old
from robin_sd_upload.supportive_scripts import check_upload_file

def arg_parse(config_file):
    parser = argparse.ArgumentParser(
        description='Robin Radar Systems Software Uploader',
        usage='robin-sd-upload [options]',
        prog='Robin Radar Systems Software Uploader',
        epilog='To report any bugs or issues, please visit: \
        https://support.robinradar.systems or run: robin-sd-upload --slack'
    )

    parser.add_argument('-c', '--check', action='store_true', help='ensure all prerequisites are met')
    parser.add_argument('-u', '--upload', action='store_true', help='upload software: robin-sd-upload --upload --type=radar_type --version=version_name --source=upload_file_folder_path')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=_version.__version__))
    parser.add_argument('-s', '--slack', action='store_true', help='Send the logs to IT/DevOps Slack channel')

    # arguments for upload
    parser.add_argument('-t', "--type", type=str, help="radar type")
    parser.add_argument("-n", "--number", type=str, help="version number of the software")
    parser.add_argument('-p', "--path", type=str, help="upload file absolute path")

    args = parser.parse_args()

    radarType = args.type
    version_name = args.number
    upload_file_path = args.path


    if args.check:
        parse_config_old(config_file)
        logger.log(message="All prerequisites met.", log_level="info", to_file=True, to_terminal=True)
        exit(0)
    elif args.upload:
        #check if type,version,source are given
        if radarType is None or version_name is None or upload_file_path is None:
            print('Please provide all the arguments: --type, --version, --source')
            exit(1)
        parse_config_old(config_file)
        validate(radarType, version_name)
        # if check_upload_file return false, exit
        if check_upload_file(upload_file_path, version_name) is False:
            exit(1)

        temp_dir = tempfile.mkdtemp()
        version_dir_to_upload= os.path.join(upload_file_path, version_name)
        zipped_file_path = os.path.join(temp_dir, version_name + '.zip')

        print('version_dir_to_upload: ', version_dir_to_upload)
        print('zipped_file_path: ', zipped_file_path)
        
        create_zip(zipped_file_path, version_name)
        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
                push_software(config, zipped_file_path, radarType, version_name)
                remove_zip(zipped_file_path)
                logger.log(message="Software uploaded successfully.", log_level="info", to_file=True, to_terminal=True)
                exit(0)
            except yaml.YAMLError as exc:
                print(exc)
                exit(1)
    elif args.slack:
        slack_handler.send_slack_entrypoint()
        logger.log(message="Slack message sent successfully.", log_level="info", to_file=True, to_terminal=True)
        exit(0)
    else:
        parser.print_help()
        exit(1)





