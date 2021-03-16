import os
import re
import importlib.util
from pathlib import Path
import shutil

from arcgis.gis import GIS, Group
from arcgis.env import active_gis
from dotenv import find_dotenv, load_dotenv

# see if arcpy available to accommodate non-windows environments
if importlib.util.find_spec('arcpy') is not None:
    import arcpy

    has_arcpy = True
else:
    has_arcpy = False

# load the .env into the namespace
load_dotenv(find_dotenv())


def _not_none_and_len(string: str) -> bool:
    """helper to figure out if not none and string is populated"""
    is_str = isinstance(string, str)
    has_len = False if re.match(r'\S{5,}', '') is None else True
    status = True if has_len and is_str else False
    return status


def get_gis():
    """Try to get a GIS object first from an active_gis and then trying to create from the .env file."""
    # if there is an active_gis, just use it
    if isinstance(active_gis, GIS):
        gis = active_gis

    # if not an active_gis, see what may be available in the .env file
    else:
        url = os.getenv('ESRI_GIS_URL')
        usr = os.getenv('ESRI_GIS_USERNAME')
        pswd = os.getenv('ESRI_GIS_PASSWORD')

        # if credentials are found, use them to create a gis (url is not needed since defaults to AGOL)
        if url is not None and usr is not None and pswd is not None:
            gis = GIS(url, username=usr, password=pswd)
        elif usr is not None and pswd is not None:
            gis = GIS(username=usr, password=pswd)
        else:
            gis = None

    return gis


def add_group(gis: GIS = None, group_name: str = None) -> Group:
    """
    Add a group to the GIS for the project for saving resources.

    Args:
        gis: Optional
            arcgis.gis.GIS object instance.
        group_name: Optional
            Group to be added to the cloud GIS for storing project resources. Default
            is to load from the .env file. If a group name is not provided, and one is
            not located in the .env file, an exception will be raised.

    Returns: Group
    """
    # if no group name provided
    if group_name is None:

        # load the group name
        group_name = os.getenv('ESRI_GIS_GROUP')

        err_msg = 'A group name must either be defined in the .env file or explicitly provided.'
        assert isinstance(group_name, str), err_msg
        assert len(group_name), err_msg

    # create an instance of the group manager
    gmgr = gis.groups

    # determine if group exists
    grp_srch = [g for g in gmgr.search() if g.title.lower() == group_name.lower()]

    # if the group does not exist
    if len(grp_srch) == 0:

        # create the group
        grp = gmgr.create(group_name)

        # ensure the group was successfully created
        assert isinstance(grp, Group), 'Failed to create the group in the Cloud GIS.'

    # if the group already exists, just get it
    else:
        grp = grp_srch[0]

    return grp


def add_directory_to_gis(dir_name: str = None, gis: GIS = None):
    """Add a directory in a GIS user's content."""
    # get the directory from the .env file using the project name
    if dir_name is None:
        dir_name = os.getenv('PROJECT_NAME')

    assert isinstance(dir_name, str), 'A name for the directory must be provided explicitly in the "dir_name" ' \
                                      'parameter if there is not a PROJECT_NAME specified in the .env file.'

    # try to figure out what GIS to use
    if gis is None:
        gis = get_gis()

    assert isinstance(gis, GIS), 'A GIS instance, either an active_gis in the session, credentials in the .env file, ' \
                                 'or an active GIS instance explicitly passed into the "gis" parameter.'

    # create the directory
    res = gis.content.create_folder(dir_name)

    # if the response is None, the folder already exists, so don't worry about it
    if res is None:
        status = True

    # otherwise, set status based on if the title is in the response
    else:
        status = 'title' in res.keys()

    return status


def create_local_data_resources(data_pth: Path = None) -> Path:
    """create all the data resources for the available environment"""
    # default to the expected project structure
    if data_pth is None:
        data_pth = Path(__file__).parent.parent.parent / 'data'

    # cover if a string is inadvertently passed in as the path
    data_pth = Path(data_pth) if isinstance(data_pth, str) else data_pth

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

            # do the same thing for a mobile geodatabase, a sqlite database
            gdb_pth = dir_pth / f'{data_name}.geodatabase'
            if gdb_pth.exists():
                gdb_pth.unlink()
            arcpy.management.CreateMobileGDB(str(dir_pth), f'{data_name}.geodatabase')

    return data_pth


class Paths:
    """Object to easily reference data resources"""

    def __init__(self):
        self.dir_prj = Path(__file__).parent.parent.parent

        self.dir_data = self.dir_prj / 'data'

        self.dir_raw = self.dir_data / 'raw'
        self.dir_ext = self.dir_data / 'external'
        self.dir_int = self.dir_data / 'interim'
        self.dir_out = self.dir_data / 'processed'

        self.gdb_raw = self.dir_raw / 'raw.gdb'
        self.gdb_ext = self.dir_ext / 'external.gdb'
        self.gdb_int = self.dir_int / 'interim.gdb'
        self.gdb_out = self.dir_out / 'processed.gdb'

        self.dir_models = self.dir_prj / 'models'

        self.dir_reports = self.dir_prj / 'reports'

        self.dir_fig = self.dir_reports / 'figures'

    @staticmethod
    def _create_resource(pth: Path) -> Path:
        """Internal function to create resources."""

        # see if we're working with a file geodatabase
        is_gdb = (pth.suffix == '.gdb' or pth.suffix == '.geodatabase')

        # if a geodatabase, the path dir is one level up
        pth_dir = pth.parent if is_gdb else pth

        # ensure the file directory exists including parents as necessary
        if not pth_dir.exists():
            pth_dir.mkdir(parents=True)

        # now if a geodatabase, create it
        if is_gdb:

            # flag if-exists so only run function once
            gdb_exists = arcpy.Exists(str(pth))

            # if a file geodatabase, create it
            if pth.suffix == '.gdb' and not gdb_exists:
                arcpy.management.CreateFileGDB(pth_dir, pth.stem)

            # if a mobile geodatabase, create it
            if pth.suffix == '.geodatabase' and not gdb_exists:
                arcpy.management.CreateMobileGDB(pth_dir, pth.stem)

        return pth

    def create_resources(self):
        """Create data storage resources if they do not already exist."""
        # get the data resources from the object properties
        pth_lst = [p for p in dir(self) if isinstance(p, Path)]

        # iterate the paths and create any necessary resources
        for pth in pth_lst:
            self._create_resource(pth)

        return
