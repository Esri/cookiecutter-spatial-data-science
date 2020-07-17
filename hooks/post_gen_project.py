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
import os
from pathlib import Path
import re
import shutil
import tempfile
import importlib
from zipfile import ZipFile

# backwards compatible version number
backwards_compatible_vers = '2.4.0'

# see if arcpy available to accommodate non-windows environments
try:
    if importlib.util.find_spec("arcpy") is not None:
        import arcpy
        has_arcpy = True
    else:
        has_arcpy = False
except AttributeError:
    if importlib.find_loader("arcpy") is not None:
        import arcpy
        has_arcpy = True
    else:
        has_arcpy = False


def _configure_aprx():

    # create project location path strings
    existing_project_path = os.path.abspath(r'./arcgis/cookiecutter.aprx')
    new_project_path = os.path.abspath(r'./arcgis/{{ cookiecutter.project_name }}.aprx')

    # copy the existing template project
    old_aprx = arcpy.mp.ArcGISProject(existing_project_path)
    old_aprx.saveACopy(new_project_path)

    # now create a reference to the new project
    new_aprx = arcpy.mp.ArcGISProject(new_project_path)

    # create the file geodatabases if they do not exist - ensures backwards compatibility
    for data_name in ['interim', 'raw', 'processed', 'external']:
        dir_path = os.path.join(os.getcwd(), 'data', data_name)
        gdb_path = os.path.join(dir_path, f'{data_name}.gdb')        
        if not arcpy.Exists(gdb_path):
            arcpy.management.CreateFileGDB(dir_path, f'{data_name}.gdb')

        # set the default file geodatabase for the aprx to interim
        if data_name == 'interim':
            new_aprx.defaultGeodatabase = gdb_path

    # create a path toolbox with the same name as the aprx
    new_name = os.path.basename(new_project_path).split('.')[0]
    new_toolbox_path = os.path.abspath(os.path.join(
        os.path.dirname(new_project_path),
        f'{new_name}.tbx'
    ))

    # copy the cookiecutter toolbox to the new location with the new name
    shutil.copyfile(old_aprx.defaultToolbox, new_toolbox_path)

    # update the pro project's default toolbox to this new path
    new_aprx.defaultToolbox = new_toolbox_path

    # save new settings for aprx
    new_aprx.save()

    # now delete the old toolbox and project
    os.remove(old_aprx.defaultToolbox)
    os.remove(existing_project_path)

    return Path(new_project_path)


def _modify_file(orig_name, tmp_dir, min_vers=None, drop_regex=None):

    # get the paths to the original and the one to write to
    orig_pth = os.path.join(os.path.abspath(tmp_dir), orig_name)
    tmp_pth = orig_pth.replace('.xml', '_modified.xml')

    # version replace string
    vrs_regex = re.compile(r'\d\.\d\.\d')

    # create and open the destination file
    with open(tmp_pth, 'w') as out_file:

        # read the input file line by line
        for line in open(orig_pth, 'r'):

            # if a regular expression to use for recognizing and removing a string, do it
            if drop_regex:
                line = drop_regex.sub('', line)
        
            # roll back references to minimum versions for backwards compatibility
            if min_vers:
                line = vrs_regex.sub(min_vers, line)
        
            # save modified line
            out_file.write(line)

    # remove and replace the original with the updated file
    os.remove(orig_pth)
    os.rename(tmp_pth, orig_pth)

    return orig_pth


def _cleanup_aprx_catalog_tree(aprx_path, min_vers=None):

    # ensure we're working with a pathlib.Path object
    aprx_path = str(aprx_path) if isinstance(aprx_path, Path) else aprx_path

    # temporary storage location for extracting contents of aprx to work with
    tmp_dir = tempfile.mkdtemp()

    # extract everything from the aprx to the temp directory
    with ZipFile(aprx_path, 'r') as aprx:
        aprx.extractall(tmp_dir)

    # regular expression used to rip out the unneeded references to the cookiecutter resources
    re_ck = re.compile(
        r"<CIMProjectItem xsi:type=\"typens:CIMProjectItem\"><CatalogPath>[\.\\/a-zA-Z{}\-_]*?cookiecutter\.(?:tbx|gdb)<\/CatalogPath>.*?<\/CIMProjectItem>")

    # modify the files in the aprx to be ready for using
    _modify_file('GISProject.xml', tmp_dir, min_vers, re_ck)
    _modify_file('DocumentInfo.xml', tmp_dir, min_vers)

    # remove the original aprx file
    os.remove(aprx_path)

    # zip up the resources in the temp directory to create the new aprx archive
    aprx_zip = shutil.make_archive(aprx_path, 'zip', tmp_dir)

    # rename the file from a zip file to the orignial aprx name
    os.rename(aprx_zip, aprx_path)

    # remove the temp directory
    shutil.rmtree(tmp_dir)

    return aprx_path


# if the cookiecutter.gdb or interim.gdb exists, get rid of it
gdb_ck = os.path.join(os.getcwd(), 'arcgis', 'cookiecutter.gdb')
gdb_int = os.path.join(os.getcwd(), 'data', 'interim.gdb')
for gdb in [gdb_ck, gdb_int]:
    if os.path.exists(gdb):
        shutil.rmtree(gdb)

# ensure the data directories are present
dir_lst = [os.path.join(os.getcwd(), 'data', drctry)
           for drctry in ['raw', 'external', 'interim', 'processed']]
for drctry in dir_lst:
    if not os.path.exists(drctry):
        os.makedirs(drctry)

# if arcpy available, set up arcgis pro resources for the project
if has_arcpy:

    aprx_pth = _configure_aprx()
    _cleanup_aprx_catalog_tree(aprx_pth, backwards_compatible_vers)

# if arcpy is not available get rid of the arcgis directory, but leave everything else
else:
    shutil.rmtree(os.path.abspath(r'./arcgis'))

# rename the env file to .env
os.rename('./env', './.env')
