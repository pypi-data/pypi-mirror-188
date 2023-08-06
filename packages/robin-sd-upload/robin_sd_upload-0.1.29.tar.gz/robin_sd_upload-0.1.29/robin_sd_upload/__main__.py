#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from .arg_parse import arg_parse

home_dir = os.path.expanduser("~")
config_file = home_dir + "/.config/robin/software_deployment.yaml"

def main():
    arg_parse(config_file)

if __name__ == "__main__":
    main()