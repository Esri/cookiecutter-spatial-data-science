# -*- coding: utf-8 -*-
__version__ = "0.0.0"
__author__ = "{{ cookiecutter.author_name }}"
__license__ = "Apache 2.0"

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


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "{{cookiecutter.project_name}}"
        self.alias = "{{cookiecutter.support_library}}"

        # List of tool classes associated with this toolbox
        self.tools = [
            CreateDataDirectory,
        ]


class CreateDataDirectory:
    def __init__(self):
        self.label = "Create GTFS Folder Structure"
        self.description = (
            "Create data directory structure for processing data."
        )
        self.category = "Utilities"  # creates toolset named "Utilities"

    def getParameterInfo(self):
        dir_data = arcpy.Parameter(
            displayName="Data Directory (where to create the child data directories)",
            name="dir_data",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input",
        )

        params = [dir_data]

        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # configure logging so messages bubble up through ArcPy
        {{cookiecutter.support_library}}.utils.configure_logging("INFO")

        # retrieve the data directory path from parameters
        dir_data = parameters[0].valueAsText

        # create the directory structure for working with GTFS datasets
        {{cookiecutter.support_library}}.utils.build_data_resources(dir_data)

        return
