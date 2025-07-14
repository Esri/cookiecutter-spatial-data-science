# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Getting Started

1 - Clone this repo.

2 - Create an environment with the requirements.
    
```
        > make env
```

3 - Explore - If you are more into Python, a good place to start is `jupyter lab` from the root of the project, and 
  look in the `./notebooks` directory. If GIS is more your schtick, open the project 
  `./arcgis/{{cookiecutter.project_name}}.aprx`.

## Using Make - common commands

Based on the pattern provided in the 
[Cookiecutter Data Science template by Driven Data](https://drivendata.github.io/cookiecutter-data-science/) this 
template streamlines a number of commands using the `make` command pattern.

- `make env` - Clone the default ArcGIS Pro Conda environment, `arcgispro-pyu3`, add all the dependencies in
  `environment.yml` and install the local project package using the command 
  `python -m pip install -e ./src/src/<project_package>` so you can easily test against the package as you are 
  developing it.

- `make data` - Run `./scripts/make_data.py`, which should be the data pipeline to create an output dataset.

- `make pytpkg` - Create a zipped achive of the Python (`*.pyt`) toolbox located in `./arcgis`. This uses the script,
  `./scripts/make_pyt_archive.py`, to collect the Python toolbox (`*.pyt`) along with all the supporting 
  dependencies listed in `pyproject.toml` and `*.xml` files with the tool documentation, and put into a zipped archive 
  ready for sharing.

- `make docserve` - Run live MkDocs documentation server to view documentation updates at http://127.0.0.1:8000.

- `make docs` - Build the documentation using MkDocs from files in `./docsrc` and save the output in `./docs`.

- `make test` - activates the environment created by the `make env` or `make env_clone` and runs all the tests in the 
  `./testing` directory using PyTest. 

## BumpVersion Cliff Notes

[Bump2Version](https://github.com/c4urself/bump2version) is preconfigured based on hints from 
[this article on Medium](https://williamhayes.medium.com/versioning-using-bumpversion-4d13c914e9b8).

If you want to...

- apply a patch, `bumpversion patch`
- update version with no breaking changes (minor version update), `bumpversion minor`
- update version with breaking changes (major version update), `bumpversion major`
- create a release (tagged in version control - Git), `bumpversion --tag release`

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-geoai">cookiecutter 
GeoAI project template</a>. This template, in turn, is simply an extension and light modification of the 
<a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project 
template</a>. #cookiecutterdatascience</small></p>
