# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Getting Started

1 - Clone this repo.

2 - Create an environment with the requirements.
    
```
        > make env
```

3 - Explore - If you are more into Python, a good place to start is `jupyter lab` from the root of the project, and look in the `./notebooks` directory. If GIS is more your schtick, open the project `./arcgis/{{cookiecutter.project_name}}.aprx`.

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

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-geoai">cookiecutter GeoAI project template</a>. This template, in turn, is simply an extension and light modification of the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
