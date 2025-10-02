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
import logging
from pathlib import Path
import shutil
import subprocess
import importlib.util

# set up logging
logger = logging.getLogger('cookiecutter.post_gen_project')
logger.setLevel(logging.DEBUG)

# see if arcpy available to accommodate non-windows environments
if importlib.util.find_spec('arcpy') is not None:
    import arcpy
    has_arcpy = True
else:
    has_arcpy = False

# pull in values from cookiecutter
new_prj_name = '{{cookiecutter.project_name}}'
new_prj_title = '{{cookiecutter.project_title}}'
new_prj_desc = '{{cookiecutter.description}}'
create_gh_repo = '{{cookiecutter.create_github_repo}}'


def setup_data(data_pth: Path) -> Path:
    """create all the data resources for the available environment from scratch to ensure version compatibility"""

    # iterate the data subdirectories
    for data_name in ['interim', 'raw', 'processed', 'external']:

        # ensure the data subdirectory exists
        dir_pth = data_pth / data_name
        if not dir_pth.exists():
            dir_pth.mkdir(parents=True)

        # if working in an arcpy environment
        if has_arcpy:

            # remove the file geodatabase if it exists and recreate it to make sure compatible with version of Pro
            fgdb_pth = dir_pth / f'{data_name}.gdb'
            if fgdb_pth.exists():
                shutil.rmtree(fgdb_pth)
            arcpy.management.CreateFileGDB(str(dir_pth), f'{data_name}.gdb')

    return data_pth


def copy_aprx(dir_arcgis: Path, new_prj_name: str, old_prj_name: str = 'cookiecutter',
              remove_originals: bool = True) -> Path:
    """Copy the APRX with the new name."""
    # aprx paths
    old_aprx_pth = dir_arcgis / f'{old_prj_name}.aprx'
    new_aprx_pth = dir_arcgis / f'{new_prj_name}.aprx'

    # get a project object instance to monkey with
    aprx = arcpy.mp.ArcGISProject(str(old_aprx_pth))

    # copy the original tbx with a new name if not the same name and set the aprx to use it
    old_tbx_pth = Path(aprx.defaultToolbox)
    new_tbx_pth = old_tbx_pth.parent / old_tbx_pth.name.replace(old_prj_name, new_prj_name)

    if old_tbx_pth != new_tbx_pth:
        shutil.copy(old_tbx_pth, new_tbx_pth)
        assert new_tbx_pth.exists()
        aprx.defaultToolbox = str(new_tbx_pth)

    # configure default geodatabase if not already set up
    gdb_pth = dir_arcgis.parent/'data'/'interim'/'interim.gdb'
    old_gdb_pth = Path(aprx.defaultGeodatabase)

    if old_gdb_pth != gdb_pth:
        assert gdb_pth.exists()
        aprx.defaultGeodatabase = str(gdb_pth)

    aprx.saveACopy(str(new_aprx_pth))

    # if removing original resources
    if remove_originals:
        del aprx  # have to remove object instance to remove referenced file
        old_aprx_pth.unlink()
        # old_tbx_pth.unlink()

    return new_aprx_pth


def create_github_repo(repo_name: str) -> None:
    """Create a GitHub repository using the gh CLI tool."""
    try:
        subprocess.run(['gh', 'repo', 'create', repo_name, "--description", new_prj_desc, '--public', '--source=.', '--remote=origin', '--push'],
                       check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Failed to create GitHub repository: {e}")


def init_git_repo(prj_path: Path) -> None:
    """Initialize a git repository in the project directory."""
    try:
        subprocess.run(['git', 'init', "--initial-branch=main"], cwd=prj_path, check=True)
        subprocess.run(['git', 'add', '.'], cwd=prj_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'initial commit'], cwd=prj_path, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to initialize git repository: {e}")


if __name__ == '__main__':

    # set up some paths to resources
    dir_prj = Path.cwd()
    dir_data_pth = dir_prj/'data'
    dir_arcgis_pth = dir_prj/'arcgis'
    env_pth = dir_prj/'env'
    config_pth = dir_prj / 'config' / 'secrets_template.ini'

    # ensure the data directories and geodatabases are all set up
    setup_data(dir_data_pth)

    # set up the ArcGIS Pro project if arcpy is available
    if has_arcpy:
        new_aprx_pth = copy_aprx(dir_arcgis_pth, new_prj_name)

    # otherwise, remove arcgis resources
    else:
        shutil.rmtree(dir_arcgis_pth)

    # rename the secrets configuration file
    config_pth.rename(dir_prj / 'config' / 'secrets.ini')

    # initialize git
    init_git_repo(dir_prj)
    logger.info('Git repository initialized.')

    # if also creating a GitHub repository, do so
    if create_gh_repo.lower() == 'yes':
        create_github_repo(new_prj_name)
        logger.info(f'GitHub repository {new_prj_name} created.')
    else:
        logger.info('GitHub repository not created.')

    logger.info(f'Project "{new_prj_title}" created!')
