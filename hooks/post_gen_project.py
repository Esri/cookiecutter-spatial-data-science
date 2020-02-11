import os
from pathlib import Path
import re
import shutil
import tempfile
import importlib
from zipfile import ZipFile

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


def _cleanup_cookiecutter_references_in_aprx(aprx_path: Path):
    """Clean up lingering references to cookiecutter toolbox and file geodatabase in the aprx."""

    # ensure we're working with a pathlib.Path object
    aprx_path = str(aprx_path) if isinstance(aprx_path, Path) else aprx_path

    # temporary storage location for extracting contents of aprx to work with
    tmp_dir = tempfile.mkdtemp()

    # extract everything from the aprx to the temp directory
    with ZipFile(aprx_path, 'r') as aprx:
        aprx.extractall(tmp_dir)

    xml_pro_name = 'GISProject.xml'

    # string path to where file resides we are going to be modifying along with the output modified file
    xml_pro_pth = os.path.join(os.path.abspath(tmp_dir), xml_pro_name)
    tmp_pth = xml_pro_pth.replace('.xml', '_modified.xml')

    # regular expression used to rip out the unneeded references to the original resources
    regex = re.compile(
        r"<CIMProjectItem xsi:type=\"typens:CIMProjectItem\"><CatalogPath>[\.\\/a-zA-Z{}\-_]*?cookiecutter\.[a-zA-Z]{3}<\/CatalogPath>.*?<\/CIMProjectItem>")

    # open and read the original xml file
    with open(tmp_pth, 'w') as out_file:
        # open the temp file where the modifications will be saved
        for line in open(xml_pro_pth, 'r'):
            # drop any matching strings in the line
            line = regex.sub(line, '') if regex.match(line) else line

            # write the line to the output file
            out_file.write(line)

    # remove the original file and save the updated one in it's place
    os.remove(xml_pro_pth)
    os.rename(tmp_pth, xml_pro_pth)

    # remove the original aprx file
    os.remove(aprx_path)

    # zip up the resources in the temp directory to create the new aprx archive
    aprx_zip = shutil.make_archive(aprx_path, 'zip', tmp_dir)

    # rename the file from a zip file to the orignial aprx name
    os.rename(aprx_zip, aprx_path)

    # remove the temp directory
    shutil.rmtree(tmp_dir)

    return aprx_path


# if the cookiecutter.gdb exists, get rid of it
gdb_ck = os.path.join(os.getcwd(), 'arcgis', 'cookiecutter.gdb')
if os.path.exists(gdb_ck):
    shutil.rmtree(gdb_ck)

# ensure the data directories are populated
dir_lst = [os.path.join(os.getcwd(), 'data', drctry)
           for drctry in ['raw', 'external', 'interim', 'processed']]
for drctry in dir_lst:
    if not os.path.exists(drctry):
        os.makedirs(drctry)

# if arcpy available, set up arcgis pro resources for the project
if has_arcpy:

    # create project location path strings
    existing_project_path = os.path.abspath(r'./arcgis/cookiecutter.aprx')
    new_project_path = os.path.abspath(r'./arcgis/{{ cookiecutter.project_name }}.aprx')

    # copy the existing template project
    old_aprx = arcpy.mp.ArcGISProject(existing_project_path)
    old_aprx.saveACopy(new_project_path)

    # now create a reference to the new project
    new_aprx = arcpy.mp.ArcGISProject(new_project_path)

    # create the file geodatabases if they do not exist - ensures backwards compatibility
    for data_name in ['interim', 'raw', 'processed']:
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

    # clean out any lingering Catalog references to cookiecutter resources
    _cleanup_cookiecutter_references_in_aprx(new_project_path)

# if arcpy is not available get rid of the arcgis directory, but leave everything else
else:
    shutil.rmtree(os.path.abspath(r'./arcgis'))
