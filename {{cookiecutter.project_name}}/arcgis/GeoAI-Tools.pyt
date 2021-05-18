# -*- coding: utf-8 -*-
import os
from pathlib import Path
import re
import sys
import tempfile

from arcgis.geometry import Geometry
from arcgis.gis import GIS
import arcpy
from dotenv import find_dotenv, load_dotenv

# get path to included resources and add to sys.path for imports
prj_pth = Path(__file__).parent.parent
src_pth = prj_pth/'src'
sys.path.insert(0, str(src_pth))

# import geoai-cookiecuter support package
import ck_tools

# load the dotenv file
load_dotenv(find_dotenv())

# ensure outputs can be overwritten
arcpy.env.overwriteOutput = True


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GeoAI-Tools"
        self.alias = "GeoAI-Tools"

        # List of tool classes associated with this toolbox
        self.tools = [AddGroupToGis, CreateDataResources, CreateAoiMask]


class AddGroupToGis(object):

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add Group to GIS"
        self.category = "Web GIS"
        self.description = "Add the Project Group to the Active GIS in ArcGIS Pro"
        self.canRunInBackground = False

        # get a reference to the current project, map and geodatabase
        try:
            self.gis = GIS('pro')
        except:
            self.gis = None

    def getParameterInfo(self):
        """Define parameter definitions"""
        grp_nm = arcpy.Parameter(
            name='grp_nm',
            displayName='ArcGIS Online Group Name',
            direction='Output',
            datatype='GPString',
            parameterType='Required',
            enabled=True
        )

        # get the group name from the .env file and set the value
        grp_nm.value = os.getenv('ESRI_GIS_GROUP')

        params = [grp_nm]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        gis_valid = False if self.gis is None else True
        return gis_valid

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return True

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # retrieve the parameters
        grp_nm = parameters[0].valueAsText

        # add the group with minimal inputs
        self.gis.groups.add(grp_nm, tags='geoai-cookiecutter')


class CreateDataResources(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Data Resources"
        self.description = "Create the data directory, child directories and geodatabases if they do not already exist."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        return

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return True

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # create all the data resources
        ck_tools.create_local_data_resources()


class CreateAoiMask(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create AOI Mask"
        self.description = "Create area of interest mask."
        self.canRunInBackground = False

        # get a reference to the current project, map and geodatabase
        aprx = arcpy.mp.ArcGISProject('CURRENT')
        self.aprx_map = aprx.activeMap
        self.gdb = aprx.defaultGeodatabase

    def getParameterInfo(self):
        """Define parameter definitions"""
        aoi_lyr = arcpy.Parameter(
            name='aoi_lyr',
            displayName='Area of Interest',
            direction='Input',
            datatype='GPFeatureLayer',
            parameterType='Required',
            enabled=True
        )
        out_fc = arcpy.Parameter(
            name='out_fc',
            displayName='Output Mask Feature Class',
            direction='Output',
            datatype='DEFeatureClass',
            parameterType='Required',
            enabled=True
        )

        params = [aoi_lyr, out_fc]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return True

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # retrieve the parameters
        aoi_fc = parameters[0].value
        out_fc = parameters[1].valueAsText

        # invoke the function
        lyr = ck_tools.create_aoi_mask_layer(aoi_fc, out_fc)

        # add the mask to the map at the top so it masks everything
        self.aprx_map.addLayer(lyr, 'TOP')
