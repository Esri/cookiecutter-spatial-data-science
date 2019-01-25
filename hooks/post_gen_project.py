import os
import shutil
import importlib

# see if arcpy available to accommodate non-windows environments
if importlib.util.find_spec("arcpy") is not None:
    import arcpy
    has_arcpy = True
else:
    has_arcpy = False

# ensure the data directories are populated
dir_lst = [os.path.join(os.getcwd(), 'data', drctry)
           for drctry in ['raw', 'external', 'interim', 'processed']]
for drctry in dir_lst:
    if not os.path.exists(drctry):
        os.makedirs(drctry)

# if arcpy available
if has_arcpy:

    # create locations
    existing_project_path = os.path.abspath(r'./arcgis/cookiecutter.aprx')
    new_project_path = os.path.abspath(r'./arcgis/{{ cookiecutter.project_name }}.aprx')

    # copy the existing template project
    old_aprx = arcpy.mp.ArcGISProject(existing_project_path)
    old_aprx.saveACopy(new_project_path)

    # now create a reference to the new project
    new_aprx = arcpy.mp.ArcGISProject(new_project_path)

    # create the file geodatabase
    interim_gdb = os.path.join(dir_lst[2], 'interim.gdb')
    if not arcpy.Exists(interim_gdb):
        arcpy.management.CreateFileGDB(dir_lst[2], 'interim.gdb')

    # set the default file geodatabase for the aprx
    new_aprx.defaultGeodatabase = interim_gdb

    # create a matched name toolbox, and set the new project to reference it
    new_name = os.path.basename(new_project_path).split('.')[0]

    # create the new toolbox path
    new_toolbox_path = os.path.abspath(os.path.join(
        os.path.dirname(new_project_path),
        new_name + '.tbx'
    ))

    # copy the toolbox to the new location
    shutil.copyfile(old_aprx.defaultToolbox, new_toolbox_path)

    # update the pro project toolbox path
    new_aprx.defaultToolbox = new_toolbox_path

    # save new settings for aprx
    new_aprx.save()

    # now delete the old toolbox and project
    os.remove(old_aprx.defaultToolbox)
    os.remove(existing_project_path)

# if arcpy is not available
else:
    shutil.rmtree(os.path.abspath(r'./arcgis'))
