"""
Licensing

Copyright 2020 Esri

Licensed under the Apache License, Version 2.0 (the "License"); You
may not use this file except in compliance with the License. You may
obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

A copy of the license is available in the repository's
LICENSE file.
"""
from configparser import ConfigParser
import logging
from pathlib import Path
import pkgutil
import sys

# path to the root of the project
dir_prj = Path(__file__).parent.parent

# if the project package is not installed in the environment
if pkgutil.find_loader('{{cookiecutter.support_library}}') is None:
    
    # get the relative path to where the source directory is located
    src_dir = dir_prj / 'src'

    # throw an error if the source directory cannot be located
    if not src_dir.exists():
        raise EnvironmentError('Unable to import {{cookiecutter.support_library}}.')

    # add the source directory to the paths searched when importing
    sys.path.insert(0, str(src_dir))

# import {{cookiecutter.support_library}}
import {{cookiecutter.support_library}}

# read and configure 
config = ConfigParser()
config.read('config.ini')

log_level = config.get('DEFAULT', 'LOG_LEVEL')
input_data = dir_prj / config.get('DEFAULT', 'INPUT_DATA')
output_data = dir_prj / config.get('DEFAULT', 'OUTPUT_DATA')

# use the log level from the config to set up basic logging
logging.basicConfig(level=log_level)
