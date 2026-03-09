# -*- coding: utf-8 -*-
__version__ = "0.0.0"
__author__ = "{{cookiecutter.author_name}}"
{% if cookiecutter.open_source_license != "No license file" %}
__license__ = "{{ cookiecutter.open_source_license }}"
{% endif %}

import importlib.util
from pathlib import Path
import sys

import arcpy


def find_pkg_source(package_name) -> Path:
    """Helper to find relative package name"""
    # get the path to the current directory
    file_dir = Path(__file__).parent

    # try to find the package in progressively higher levels
    for idx in range(4):
        tmp_pth = file_dir / "src" / package_name
        if tmp_pth.exists():
            return tmp_pth.parent
        else:
            file_dir = file_dir.parent

    # if nothing fund, nothing returned
    return None


# account for using relative path to package
if importlib.util.find_spec("{{cookiecutter.support_library}}") is None:
    src_dir = find_pkg_source("{{cookiecutter.support_library}}")
    if src_dir is not None:
        sys.path.append(str(src_dir))

# include custom code
import {{cookiecutter.support_library}}
from {{cookiecutter.support_library}}.utils import get_logger


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "{{cookiecutter.project_name}}"
        self.alias = "{{cookiecutter.support_library}}"

        # List of tool classes associated with this toolbox
        self.tools = [
            ExampleTool,
            ExampleToolInToolset,
        ]


class ExampleTool:
    def __init__(self):
        self.label = "Example Tool"
        self.description = (
            "Create data directory structure for processing data."
        )
        self.category = "Utilities"  # creates toolset named "Utilities"

        # configure logging
        logger_name = f"{{cookiecutter.support_library}}.Toolbox.{self.__class__.__name__}"
        self.logger = get_logger(logger_name, level="INFO", add_arcpy_handler=True)

    def getParameterInfo(self):
        """Define parameter definitions"""

        features = arcpy.Parameter(
            displayName="Input Features",
            name="features",
            datatype="GPFeatureLayer",  # use this data type to include both feature classes and feature layers in ArcGIS Pro
            parameterType="Required",
            direction="Input"
        )

        params = [features]

        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # retrieve the data directory path from parameters
        dir_data = parameters[0].value

        # log some messages
        self.logger.info(f"Processing input features: {dir_data}")

        return

class ExampleToolInToolset:
    def __init__(self):
        self.label = "Example Tool in Toolset"
        self.description = (
            "An example tool within a toolset."
        )
        self.category = "Example Toolset"  # creates toolset named "Example Toolset"

        # configure logging
        logger_name = f"{{cookiecutter.support_library}}.Toolbox.{self.__class__.__name__}"
        self.logger = get_logger(logger_name, level="INFO", add_arcpy_handler=True)

    def getParameterInfo(self):
        """Define parameter definitions"""

        features = arcpy.Parameter(
            displayName="Input Features",
            name="input_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        attribute_field = arcpy.Parameter(
            displayName="Attribute Field",
            name="attribute_field",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        attribute_field.filter.type = "ValueList"

        params = [features, attribute_field]

        return params
    
    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal validation is performed.
        
        This method is called whenever a parameter has been changed.
        """
        # get the parameters for easier access
        features, attribute_field = parameters

        # populate attribute field choices based on input features
        if features.altered and features.value:
            desc = arcpy.Describe(features.valueAsText)
            fields = desc.fields
            field_names = [field.name for field in fields]
            attribute_field.filter.list = field_names
        elif not features.value:
            attribute_field.filter.list = []

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # retrieve the data directory path from parameters
        features = parameters[0].value
        attribute_field = parameters[1].value

        # describe input features
        desc = arcpy.Describe(features)

        # if the input features are a feature layer, get the underlying data source
        if desc.dataType == "FeatureLayer":
            src = desc.dataSource
            name = desc.name
        else:
            src = features
            name = Path(src).stem

        # log some messages
        self.logger.info(f"Processing input features, '{name}', from {src} using attribute field, '{attribute_field}'")

        return