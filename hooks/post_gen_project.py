"""
Licensing

Copyright 2025 Esri

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

# set up logging - tying into cookiecutter logging
logger = logging.getLogger('cookiecutter.hooks.post_gen_project')
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
github_org = '{{cookiecutter.github_organization}}'


def setup_data(data_pth: Path) -> Path:
    """create all the data resources for the available environment from scratch to ensure version compatibility"""

    if not has_arcpy:
        logger.warning('arcpy not available; skipping file data geodatabase creation')

    # iterate the data subdirectories
    for data_name in ['interim', 'raw', 'processed', 'external']:

        # ensure the data subdirectory exists
        dir_pth = data_pth / data_name
        if not dir_pth.exists():
            dir_pth.mkdir(parents=True)
            logger.info(f'Created data directory: {dir_pth}')

        # if working in an arcpy environment
        if has_arcpy:

            # remove the file geodatabase if it exists and recreate it to make sure compatible with version of Pro
            fgdb_pth = dir_pth / f'{data_name}.gdb'
            if fgdb_pth.exists():
                shutil.rmtree(fgdb_pth)
            arcpy.management.CreateFileGDB(str(dir_pth), f'{data_name}.gdb')
            logger.info(f'Created file geodatabase: {fgdb_pth}')

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
    
    logger.info(f'Created toolbox: {new_tbx_pth}')

    if old_tbx_pth != new_tbx_pth:
        shutil.copy(old_tbx_pth, new_tbx_pth)
        assert new_tbx_pth.exists()
        aprx.defaultToolbox = str(new_tbx_pth)
        
        logger.info(f'Set ArcGIS Pro default toolbox to: {new_tbx_pth}')

    # configure default geodatabase if not already set up
    gdb_pth = dir_arcgis.parent/'data'/'interim'/'interim.gdb'
    old_gdb_pth = Path(aprx.defaultGeodatabase)

    if old_gdb_pth != gdb_pth:
        assert gdb_pth.exists()
        aprx.defaultGeodatabase = str(gdb_pth)

        logger.info(f'Set ArcGIS Pro default geodatabase to: {gdb_pth}')

    aprx.saveACopy(str(new_aprx_pth))
    logger.info(f'Created ArcGIS Pro project: {new_aprx_pth}')

    # if removing original resources
    if remove_originals:
        del aprx  # have to remove object instance to remove referenced file
        old_aprx_pth.unlink()

        logger.info(f'Removed original Cookiecutter ArcGIS Pro project: {old_aprx_pth}')
        
        # old_tbx_pth.unlink()

    return new_aprx_pth


def init_git_repo(prj_path: Path) -> None:
    """Initialize a git repository in the project directory."""
    try:
        subprocess.run(['git', 'init', "--initial-branch=main"], cwd=prj_path, check=True)
        subprocess.run(['git', 'add', '.'], cwd=prj_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'initial commit'], cwd=prj_path, check=True)
        logger.info('Initialized git repository and made initial commit.')
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to initialize git repository: {e}")


def create_github_repo(repo_name: str) -> None:
    """Create a GitHub repository using the gh CLI tool."""
    try:
        subprocess.run(['gh', 'repo', 'create', repo_name, "--description", new_prj_desc, '--public', '--source=.', '--remote=origin', '--push'],
                       check=True)
        logger.info(f'Created GitHub repository: {repo_name}')
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to create GitHub repository: {e}")


if __name__ == '__main__':

    # set up some paths to resources
    dir_prj = Path.cwd()
    dir_data_pth = dir_prj/'data'
    dir_arcgis_pth = dir_prj/'arcgis'
    env_pth = dir_prj/'env'
    config_pth = dir_prj / 'config' / 'secrets_template.ini'

    # add logging hander to write progress to a file
    fh = logging.FileHandler(dir_prj / 'post_gen_project.log', mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # ensure the data directories and geodatabases are all set up
    setup_data(dir_data_pth)

    # set up the ArcGIS Pro project if arcpy is available
    if has_arcpy:
        new_aprx_pth = copy_aprx(dir_arcgis_pth, new_prj_name)

    # otherwise, remove arcgis resources
    else:
        shutil.rmtree(dir_arcgis_pth)
        logger.info('arcpy not available; removed arcgis directory.')

    # rename the secrets configuration file
    config_pth.rename(dir_prj / 'config' / 'secrets.ini')
    logger.info('Added secrets configuration file.')

    # initialize git
    init_git_repo(dir_prj)

    # if also creating a GitHub repository, do so
    if create_gh_repo.lower() == 'yes':
        repo_full_name = f'{github_org}/{new_prj_name}' if github_org else new_prj_name
        create_github_repo(repo_full_name)
    else:
        logger.info('GitHub repository not created.')

    logger.info(f'Project "{new_prj_title}" created!')
