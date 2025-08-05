# Cookiecutter-Spatial-Data-Science

Cookiecutter-Spatial-Data-Science strives to streamline and promote use of best practices for projects combining 
Geography and Data Science through a logical, reasonably standardized, and flexible project structure.

Cookiecutter-Spatial-Data-Science project grew out of a need to streamline project bootstrapping, encourage 
innovation, increase repeatability, encourage documentation, and encourage best practices.

## Requirements

 * ArcGIS Pro (optional, but highly recommended)
 * [Conda (Anaconda or miniconda)](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
 * [Cookiecutter](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0
 * [Git](https://git-scm.com/downloads)

``` cmd
conda install -c conda-forge cookiecutter
```

## To start a new project, run:

``` cmd
cookiecutter https://github.com/esri/cookiecutter-spatial-data-science
```

## Using Make - common commands

Based on the pattern provided in the 
[Cookiecutter Data Science template by Driven Data](https://drivendata.github.io/cookiecutter-data-science/) this 
template streamlines a number of commands using the `make` command pattern.

- `make env` - Clone the default ArcGIS Pro Conda environment, `arcgispro-py3`, add all the dependencies in
  `environment.yml` and install the local project package using the command 
  `python -m pip install -e ./src/src/<project_package>` so you can easily test against the package as you are 
  developing it.

- `make data` - Run `./scripts/make_data.py`, which should be the data pipeline to create an output dataset.

- `make pytzip` - Create a zipped achive of the Python (`*.pyt`) toolbox located in `./arcgis`. This uses the script,
  `./scripts/make_pyt_archive.py`, to collect the Python toolbox (`*.pyt`) along with all the supporting 
  dependencies listed in `pyproject.toml` and `*.xml` files with the tool documentation, and put into a zipped archive 
  ready for sharing.

- `make docserve` - Run live MkDocs documentation server to view documentation updates at http://localhost:8000.

- `make docs` - Build the documentation using MkDocs from files in `./docsrc` and save the output in `./docs`.

- `make test` - activates the environment created by the `make env` and runs all the tests in the 
  `./testing` directory using PyTest.

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Esri welcomes contributions from anyone and everyone. Please see our 
[guidelines for contributing](https://github.com/esri/contributing).

## Licensing

Copyright 2025 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with 
the License. You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on 
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the 
specific language governing permissions and limitations under the License.

A copy of the license is available in the repository's [LICENSE](LICENSE?raw=true) file.
