---
title: Home
---
# Cookiecutter-Spatial-Data-Science 3.2.6

Creating results effectively communicating actionable insights from data requires
creative exploration and experimentation. It is a sloppy, messy and disorganized
process, especially at first. Reproducing results, by you or by others, requires 
well organized and documented resources. Data analysis, data science or data 
engineering projects require both creative exploration and reproducability.

Trying to create structure inhibits creativity. Disorganization inhibits 
reproducability. Cookiecutter-Spatial-Data-Science is a templated structure making
it possible to quickly get started and enable the creative exploration necessary
for discovering insights from data. Once discovered, within the structure
of the project, you can reproduce documented results with minimal effort.

This is accomplished by borrowing best practices from data science, and marrying these
with the capabilities of ArcGIS Pro. This enables taking advantage of the 
geographic (spatial) analysis and visualization capablities of ArcGIS Pro
in a structured way to derive reproducable and documented insights from data.

## Getting Started

![Basic Use](assets/basic_use.gif)

Setup and basic use are well detailed with easily copyable commands in the 
[Getting Started](getting_started.md#setup-with-arcgis-pro) page.

## Project Structure

```
├───.github
│   └───workflows
│           make-mkdocs.yml               # automatically build documentation using GitHub Actions with GitHub repo
├───arcgis                                # directory for ArcGIS Pro assets and resources
│   │   cookiecutter.tbx                  
│   │   README.md
│   │   sik-prj.aprx                      # ArcGIS Pro project
│   │   sik-prj.tbx                       # traditional toolbox used by ArcGIS Pro
│   │   sik_prj.pyt                       # ArcGIS Pro Python toolbox
│   ├───layer_files                       # location to save useful layer files
│   └───styles                            # collection of styles added to ArcGIS Pro project with more cartographic options
│           Firefly.stylx
│           GlassyNorthArrows.stylx
│           PaperCut.stylx
│           PenAndInk.stylx
│           PhysicalGeographyAtlas.stylx
│           Sketch.stylx
│           Watercolor.stylx
├───config                                # config files used with project
│       config.ini                        # config settings, which are NOT sensitive
│       secrets.ini                       # config settings, which ARE sensitive (usernames, passwords, etc.)
├───data                                  # location for data storage (excluded from version control)
│   ├───external                          # data used as part of data processing, but not data being transformed
│   │   └───external.gdb
│   ├───interim                           # intermediate location for caching data
│   │   └───interim.gdb
│   ├───processed                         # final output data location
│   │   └───processed.gdb
│   └───raw                               # raw immutable data location
│       └───raw.gdb
├───docsrc                                # MkDocs source directory
│   │   mkdocs.yml                        # MkDocs configuration file
│   │   requirements.txt                  # packages needed for building using MkDocs in GitHub
│   └───mkdocs                            # where markdown files and Jupyter Notebooks for docs are stored
│       │   api.md                        # example of documenting Python from DocStrings
│       │   index.md                      # example main documentation file
│       └───notebooks                     # location to store notebooks for inclusion in documentation
├───env                                   # directory created for Conda Python environment using make env command
├───models                                # location where machine learning models are saved (excluded from version control)
│   └───emd
│           example.emd
├───notebooks
│       notebook-template.ipynb           # Jupyter Notebook example with some useful boilerplate
├───references                            # location to save useful references used as part of project development
├───reports                               # location to save graphic outputs and logging outputs from analysis
│   ├───figures
│   └───logs
├───scripts                               # standalone automation scripts
│   │   config.ini                        # configuration options specific to standalone scripts
│   │   make_data.py                      # script used to run the data processing pipeline
│   │   make_pyt_archive.py               # supporting script helping to create standalone zipped archive of .pyt toolbox
│   └───raster_functions                  # location for ArcGIS Pro raster functions
├───src                                   # where Python source code lives
│   └───sik_prj                           # Python package for reusable code
│       │   __init__.py
│       │   __main__.py                   
│       │
│       └───utils
│               logging_utils.py
│               main.py
│               __init__.py
├───testing
│       test_sik_prj.py                   # example PyTest file
│
│   .bumpversion.cfg                      # configuration for Bumpversion 
│   .gitignore                            # files and directories to exclude from version control
│   environment.yml                       # additional packages to install in development environment
│   LICENSE                               # license file text
│   make.cmd                              # make commands for Windows
│   Makefile                              # make commands for *nix
│   pyproject.toml                        # Python package configuration (dependencies listed in here)
│   README.md                             # readme displayed on front page of GitHub repo
│   VERSION                               # project version number
```