# Getting Started

At an absolute minimum, you need a working version of Conda. An installation of ArcGIS Pro
is also extremely useful, though not strictly required. I regularly use this template on
both my Windows tower with ArcGIS Pro and my MacBook Pro laptop, so I can attest it works
in both environments.

That said, I typically start projects on my Windows machine with ArcGIS Pro. This lets the
project initialize with a configured ArcGIS Pro project (an `*.aprx` file). From there, I
sync the project to a Git repository and continue working on it in either environment.

## Requirements

### Optional

#### ArcGIS Pro

Cookiecutter-Spatial-Data-Science was created out of a need to marry the best practices of
Data Science and Data Engineering with ArcGIS Pro. So, while not strictly required, an
environment with ArcGIS Pro will make this template much more useful.

### Essential

#### Conda

* [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) or
  [Anaconda](https://www.anaconda.com/docs/getting-started/anaconda/install)
* can be bundled with ArcGIS Pro (**Start > Programs > ArcGIS > Python Command Prompt**)

It does not matter how Conda is available, only that it is. Either Miniconda or Anaconda
will do, since both provide Conda, which Cookiecutter-Spatial-Data-Science uses for Python
environment management.

#### [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html)

Cookiecutter-Spatial-Data-Science is a template for project generation, and Cookiecutter is
the templating system that drives it. Creating an environment with Cookiecutter installed
is covered in the next section, [Setup with ArcGIS Pro](#setup-with-arcgis-pro).

#### [Git](https://git-scm.com/downloads)

Git is used for distributed version control. When a new project is created, it is
initialized as a local Git repository so you have version control from the start.

#### [GitHub CLI (optional)](https://cli.github.com/)

The GitHub CLI is optional but extremely useful. It lets you quickly create a remote
repository on GitHub and link your local repository to it. If you do not have it installed,
you can always perform these steps manually on the GitHub website.

## Setup with ArcGIS Pro

<iframe 
style="width: 100%; aspect-ratio: 16 / 9; border: 0;"
src="https://www.youtube.com/embed/25-p9OW2CGI?si=wKis61yUw06uQv6x"
title="YouTube video player" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

If you have ArcGIS Pro installed, Miniconda is bundled with it. Open a Conda-ready command
prompt through **Start > ArcGIS > Python Command Prompt** to make sure all the Conda
commands are available.

Cookiecutter is not included in the default Conda environment shipped with ArcGIS Pro. To
get started with the Cookiecutter-Spatial-Data-Science template, create a Conda environment
named `ck` from the Python Command Prompt.

``` cmd
conda create -n ck --clone arcgispro-py3
```

Once created, activate it.

``` cmd
activate ck
```

This new environment contains nothing beyond Python, so the next step is to add
Cookiecutter.

``` cmd
conda install -c conda-forge cookiecutter
```

You are now ready to use Cookiecutter-Spatial-Data-Science by following the steps below.

## Use

### Create A Project

From the command line, navigate to the folder where you want to create a new project, make
sure the Conda environment with Cookiecutter installed is active (`activate ck`), and
run...

``` cmd
cookiecutter https://github.com/esri/cookiecutter-spatial-data-science
```

You will be prompted to answer a few questions, and once answered your new project will be
created in its own directory. Project setup also initializes a Git repository and performs
an initial commit, so you can quickly get to work.

!!! tip
    Once created, you will normally want to jump into the project directory and continue
    working. If you are not as familiar with the command line, you can move between
    directories using the `cd` (change directory) command. For example, if your project
    directory is named `sik-project`, jump into it with `cd sik-project`.

### Create Project Conda Environment

While not always strictly necessary, it is good practice to create a Conda environment for
your project. Cookiecutter-Spatial-Data-Science includes an `environment.yml` file with a
number of packages I typically use. My philosophy is to be fairly inclusive in this file,
so before creating your project I encourage you to prune it to fit your needs.

Once you are happy with the packages in `environment.yml`, the many common tasks have been
streamlined using the Makefile pattern. Although not identical, I was able to mimic the
behavior on Windows in the included `make.bat` file. One of the most common tasks is
creating a new Conda environment.

The command...

``` cmd
make env
```

...will create your new Conda environment. Rather than using Conda's default location, this
command creates the environment inside the project at `./env`. Especially if your projects
live on a different drive than your Conda installation, this avoids filling up your main
drive with Python packages.

Once created, activate it with...

``` cmd
conda activate ./env
```

## Useful - User Config File

If you use the Cookiecutter-Spatial-Data-Science template regularly, you can avoid retyping
values like the template URL, your name, and your ArcGIS Online organization URL by
creating a file in your home directory called `.cookiecutterrc` with these values set as
defaults and abbreviations.

For example, if your computer login is `gis_yoda`, create a text file at
`C:/Users/gis_yoda/.cookiecutterrc` with the following contents.

``` yaml
default_context:
    author_name: GIS Yoda
    email: yoda@dagobah.com
    esri_web_gis_url: https://theresistance.maps.arcgis.com
abbreviations:
    sds: https://github.com/esri/cookiecutter-spatial-data-science
```

Now, to start a new project, just open the Python Command Prompt
(**Start > Programs > ArcGIS > Python Command Prompt**), activate the Python environment
with Cookiecutter installed...

``` cmd
activate ck
```

...and use Cookiecutter-Spatial-Data-Science via the `sds` abbreviation.

``` cmd
cookiecutter sds
```

When the project starts, the values from your default context will be used, so you do not
have to type them in every time.

!!! note

    Use of a user config file is well documented in the
    [Cookiecutter documentation](https://cookiecutter.readthedocs.io/en/latest/advanced/user_config.html)
    if you want to explore more options. The keys to use in the default context can be
    found in the `cookiecutter.json` file in the Cookiecutter-Spatial-Data-Science
    template.
