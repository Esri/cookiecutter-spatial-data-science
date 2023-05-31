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
import pkgutil

# if the project package is not installed in the environment
if pkgutil.find_loader('{{cookiecutter.support_library}}') is None:
    
    # late imports for finding the package relative to the script
    from pathlib import Path
    import sys
    
    # get the relative path to where the source directory is located
    src_dir = Path(__file__).parent.parent / 'src'

    # throw an error if the source directory cannot be located
    if not src_dir.exists():
        raise EnvironmentError('Unable to import {{cookiecutter.support_library}}.')

    # add the source directory to the paths searched when importing
    sys.path.insert(0, str(src_dir))

# import the project package
import {{cookiecutter.support_library}}
