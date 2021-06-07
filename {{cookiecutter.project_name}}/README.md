# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Getting Started

1 - Clone this repo.

2 - Create an environment with the requirements.
    
```
        > make env
```

3 - Explore - If you are more into Python, a good place to start is `jupyter lab` from the root of the project, and look in the `./notebooks` directory. If GIS is more your schtick, open the project `./arcgis/{{cookiecutter.project_name}}.aprx`.

## BumpVersion Cliff Notes

[Bump2Version](https://github.com/c4urself/bump2version) is preconfigured based on hints from [this article on Medium](https://williamhayes.medium.com/versioning-using-bumpversion-4d13c914e9b8).

If you want to...

- increment the minor version (no breaking changes), `bumpversion minor`
- apply a patch, `bumpversion patch`
- increment major version (breaking changes), `bumpversion major`
- create a release (tagged in vesrion control - Git), `bumpversion --tag release`

## Project Organization
------------
```
    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data`
    ├── make.bat           <- Windows batch file with commands like `make data`
    ├── setup.py           <- Setup script for the library ({{ cookiecutter.support_library }})
    ├── .env               <- Any environment variables here - created as part of project creation, 
    │                         but NOT syncronized with git repo for project.                
    ├── README.md          <- The top-level README for developers using this project.
    ├── arcgis             <- Root location for ArcGIS Pro project created as part of
    │   │                     data science project creation.
    │   ├── {{ cookiecutter.project_name }}.aprx <- ArcGIS Pro project.    
    │   └── {{ cookiecutter.project_name }}.tbx  <- ArcGIS Pro toolbox associated with the project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    ├── notebooks          <- Jupyter notebooks. Naming convention is a 2 digits (for ordering),
    │   │                     descriptive name. e.g.: 01_exploratory_analysis.ipynb
    │   └── notebook_template.ipynb
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    ├── environment.yml    <- Requirements file for reproducing the analysis execution environment.
    │                         This includes far fewer dependencies and does not include arcpy.
    ├── environment_dev.yml<- Requirements file for reproducing the analysis deveopment environment.
    │                         This includes arcpy and everything needed to generate Sphinx docs.
    └── src                <- Source code for use in this project - all scripts, modules and code.
        └── {{ cookiecutter.support_library }} <- Library containing the bulk of code used in this 
                                                  project. 
```

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-geoai">cookiecutter GeoAI project template</a>. This template, in turn, is simply an extension and light modification of the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
