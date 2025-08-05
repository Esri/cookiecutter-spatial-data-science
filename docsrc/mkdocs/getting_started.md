# Getting Started

At an absolute minimum, you need a version of Conda to work with. Also extremely useful,
but not absolutely necessary, is an installation of ArcGIS Pro as well. I frequently
use this template both on my Windows tower with ArcGIS Pro, and on my MacBook Pro laptop,
so I can attest to it working in both environments. 

Admittedly, I typically start projects on my Windows machine with ArcGIS Pro. This
enables the project to initialize with a configured ArcGIS Pro project (``*.aprx`` file).
From there, I sync the project with a Git repository, and work on it in both environments.

## Requirements

### Essential

#### Conda

* [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) or 
[Anaconda](https://www.anaconda.com/docs/getting-started/anaconda/install)
* can be bundled with ArcGIS Pro (Start > Programs > ArcGIS > Python Command Prompt)

It really does not matter how Conda is available, provided it is available. There are two
versions of Conda you may have, either Miniconda or Anaconda. Either provides Conda, what 
Cookiecutter-Spatial-Data-Science uses for Python environment management.

#### [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html)

Cookiecutter-Spatial-Data-Science is a template for project generation. The templating
system is Cookiecutter.

#### [Git](https://git-scm.com/downloads)

Git is used for distributed version control. When a project is initially created, it is
initalized as a local Git repository enabling easy version control from the start.

### Optional

#### ArcGIS Pro

Although not entirely necessary, Cookiecutter-Spatial-Data-Science was developed out of a
need to marry the best practices of Data Science and Data Engineering with ArcGIS Pro. Hence,
although not entirely necessary, an environment with ArcGIS Pro is going to make this
template much more useful.

## Setup with ArcGIS Pro

<iframe 
style="width: 100%; aspect-ratio: 16 / 9; border: 0;"
src="https://www.youtube.com/embed/kwHRZqJZ3_g?si=T_pVUgcnoqEG3Ddn" 
title="YouTube video player" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

If you have ArcGIS Pro installed, Miniconda is included and bundled with ArcGIS Pro. The
largest difference is you will need to access the command line from Start > ArcGIS > Python 
Command Prompt. This will ensure you have all the Conda commands available.

Cookiecutter is not included with the default Conda environment shipped with ArcGIS Pro.
If you want to get started with the Cookiecutter-Spatial-Data-Science template, you can
start by creating a Conda environment named `ck` in the Python Command Prompt.

``` cmd
conda create -n ck --clone arcgispro-py3
```

Once created, you can activate this environment.

``` cmd
activate ck
```

This Conda environemnt includes nothing more than Python. Next, you need to add Cookiecutter.

``` cmd
conda install -c conda-forge cookiecutter
```

Now, you are ready to start using Cookiecutter-Spatial-Data-Science by following the steps 
below.

## Use

### Create A Project

From the command line, in a folder or directory you want to create a new project, ensure the
Conda environment with Cookiecutter installed is active (`activate ck`), and then use...

``` cmd
cookiecutter https://github.com/esri/cookiecutter-spatial-data-science
```

You will be prompted to answer a few questions for setting up the project, and once answered,
your new project will be created in its own directory. The project setup includes initializing
the project with Git and performing an initial commit enabling you to quickly get to work.

!!! tip
    Once created, you normally will want to jump into this directory and continue working. If 
    not as familiar with the command line, you can move to different directories using
    the `cd` (change directory) command. Hence, if your project directory is named 
    `sik-project`, you can jump into this directory using the command `cd sik-project`.

### Create Project Conda Environment

While not always enrirely necessary, it is a good practice to create a Conda enviroment for your
project. Cookiecutter-Spatial-Data-Science includes an `environment.yml` file with a number
of packages I typically include. My philosopy is to be rather inclusive in this file. Hence,
before creating your project I encourage you to prune this file.

Once happy with the packages included in the `environment.yml` file, I have streamlined the
many common tasks using the Makefile pattern. Although not idencial, I was able to mimic the
behavior on Windows in the included `make.bat` file. One of the very common tasks is creation
of a new Conda environment.

The command...

``` cmd
make env
```

...will create your new Conda environment. Rather than using the default location for Conda
environments, this command creates the environment right in the project in the `./env`
directory. Especially if your projects reside on a different drive than where your Conda
installation resides, this can avoid filling up your main drive with Python pacakges for
Conda environments.

Once created, you can now use this environment using the command...

``` cmd
conda activate ./env
```

## Useful - User Config File

If using the Cookiecutter-Spatial-Data-Science template regularly, rather than always
typing in values such as the URL for Cookiecutter-Spatial-Data-Science, your name and 
ArcGIS Online Orginization URL, you can create a file in your home directory called 
`.cookiecutterrc`, with these values set as defaults and abbreviations.

For instance, if the login for your computer is `gis_yoda`, create a text file located
at `C:/Users/gis_yoda/ .cookiecutterrc`. Then, put the following in this file.

``` yaml
default_context:
    author_name: GIS Yoda
    email: yoda@dagobah.com
    esri_web_gis_url: https://theresistance.maps.arcgis.com
abbreviations:
    sds: https://github.com/esri/cookiecutter-spatial-data-science
```

Now, when you want to start a new project, all you have to do is open the Python Command
Prompt (Start > Programs > ArcGIS > Python Command Prompt), activate the Python enviroment
with Cookiecutter installed...

``` cmd
activate ck
```

... and use Cookiecutter-Spatial-Data-Science using the `sds` abbreviation.

``` cmd
cookiecutter sds
```

Then, when starting the project, the values in the default context will be used, so you do
not have to type them in every time.

!!! note
    
    Use of a user config file is well documented in the 
    [Cookiecutter documentation](https://cookiecutter.readthedocs.io/en/latest/advanced/user_config.html) 
    if you want to explore more options. The key values to use for the default context can be found in
    the `cookiecutter.json` file in the Cookiecutter-Spatial-Data-Science template.
