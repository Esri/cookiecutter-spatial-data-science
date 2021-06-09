# Cookiecutter-Spatial-Data-Science

Cookiecutter-Spatial-Data-Science strives to streamline and promote use of best practices for projects combining Geography and Data Science through a logical, reasonably standardized, and flexible project structure.

Cookiecutter-Spatial-Data-Science project grew out of a need within the Advanced Analytics team at Esri to streamline project bootstrapping, encourage innovation, increase repeatability, encourage documentation, and encourage best practices.

## Requirements

 * ArcGIS Pro 2.7
 * [Conda (Anaconda or miniconda)](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
 * [Cookiecutter](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0

``` cmd
> conda install -c conda-forge cookiecutter
```

## To start a new project, run:

``` cmd
> cookiecutter https://github.com/esri/cookiecutter-spatial-data-science
```

## Using Make - common commands

Based on the pattern provided in the [Cookiecutter Data Science template by Driven Data](https://drivendata.github.io/cookiecutter-data-science/) this template streamlines a number of commands using the `make` command pattern.

- `make env` - builds the Conda environment with all the name and dependencies from `environment_dev.yml` and installs the local project package `{{cookiecutter.support_library}}` using the command `python -m pip install -e ./src/src/{{cookiecutter.support_library}}` so you can easily test against the package as you are developing it.

- `make env_clone` - designed for environments using the default Conda instance installed with ArcGIS Pro. It is similar to `make env`, except this command clones the `arcgispro-py3` environment. Otherwise, it still installs the packages listed in `environment_dev.yml` and installs the local package using `pip` as described above.

- `make docs` - builds Sphinx docs based on files in `./docsrc/source` and places them in `./docs`. This enables easy publishing in the master branch in GitHub.

- `make test` - activates the environment created by the `make env` or `make env_clone` and runs all the tests in the `./testing` directory using PyTest. Alternately, if you prefer to use [TOX](https://tox.readthedocs.io) for testing (my preference), there is a `tox.ini` file included as well. The dependencies (`tox` and `tox-conda`) for using TOX are included in the default requirements. By default, the TOX file creates an environment from the `environment.yml` file using much fewer dependencies than the `*_dev.yml` files.

## BumpVersion Cliff Notes

[Bump2Version](https://github.com/c4urself/bump2version) is preconfigured based on hints from [this article on Medium](https://williamhayes.medium.com/versioning-using-bumpversion-4d13c914e9b8).

If you want to...

- apply a patch, `bumpversion patch`
- update version with no breaking changes (minor version update), `bumpversion minor`
- update version with breaking changes (major version update), `bumpversion major`
- create a release (tagged in vesrion control - Git), `bumpversion --tag release`

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Esri welcomes contributions from anyone and everyone. Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Licensing

Copyright 2020 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

A copy of the license is available in the repository's [LICENSE](LICENSE?raw=true) file.
