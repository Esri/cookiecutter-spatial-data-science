# -*- coding: utf-8 -*-
import os

from arcgis.geometry import Geometry
import arcpy

# ensure outputs can be overwritten
arcpy.env.overwriteOutput = True


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GeoAI-Tools"
        self.alias = "GeoAI-Tools"

        # List of tool classes associated with this toolbox
        self.tools = [CreateAoiMask]


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

        # ensure the aoi is a polygon
        geom_type = arcpy.Describe(aoi_fc).shapeType
        if not geom_type == 'Polygon':
            raise Exception(f'The area of interest input must be the Polygon geometry type, not {geom_type}.')

        # create a geomery list with one geometry, a rectangle covering the globe
        mask_geom = Geometry({
            "rings": [[[-180.0, -90.0], [-180.0, 90.0], [180.0, 90.0], [180.0, -90.0], [-180.0, -90.0]]],
            "spatialReference": {"wkid": 4326, "latestWkid": 4326}
        })
        extent_features = [mask_geom.as_arcpy]

        # create a mask feature class by punching out the area of interest
        mask_fc = arcpy.analysis.Erase(extent_features, aoi_fc, out_fc)[0]

        # get a layer to work with, and apply nice symbology
        lyr = arcpy.management.MakeFeatureLayer(mask_fc)[0]
        arcpy.management.ApplySymbologyFromLayer(lyr, './layer_files/aoi_mask.lyrx')

        # add the mask to the map
        self.aprx_map.addLayer(lyr)
