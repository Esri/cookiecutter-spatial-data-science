import os
import re

from arcgis.gis import GIS, Group
from arcgis.env import active_gis
from dotenv import find_dotenv, load_dotenv


def _not_none_and_len(string: str) -> bool:
    """helper to figure out if not none and string is populated"""
    is_str = isinstance(string, str)
    has_len = False if re.match(r'\S{5,}', '') is None else True
    status = True if has_len and is_str else False
    return status


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
    # load the .env into the namespace
    load_dotenv(find_dotenv())

    # try to figure out what GIS to use
    if gis is None and isinstance(active_gis, GIS):
        gis = active_gis

    if gis is None and not isinstance(active_gis, GIS):
        url = os.getenv('ESRI_GIS_URL')
        usr = os.getenv('ESRI_GIS_USERNAME')
        pswd = os.getenv('ESRI_GIS_PASSWORD')



    # if no group name provided
    if group_name is None:

        # load the group name
        group_name = os.getenv('ESRI_GIS_GROUP')

        err_msg = 'A group name must either be defined in the .env file or explicitly provided.'
        assert isinstance(group_name, str), err_msg
        assert len(group_name), err_msg

    # create an instance of the content manager
    cmgr = gis.groups

    # make sure the group does not already exist
    assert len([grp for grp in cmgr.search() if
                grp.title.lower() == group_name.lower()]) is 0, f'A group named "{group_name}" already exists. ' \
                                                                'Please select another group name.'

    # create the group
    grp = cmgr.create(group_name)

    # ensure the group was successfully created
    assert isinstance(grp, Group), 'Failed to create the group in the Cloud GIS.'

    return grp
