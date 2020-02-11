import os
import shutil
import importlib

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

# if arcpy available
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

# if arcpy is not available get rid of the arcgis directory, but leave everything else
else:
    shutil.rmtree(os.path.abspath(r'./arcgis'))
