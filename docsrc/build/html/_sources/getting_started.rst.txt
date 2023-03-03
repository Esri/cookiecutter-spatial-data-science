Getting Started
================

At an absolute minimum, you need a version of Conda to work with. Also extremely useful,
but not absolutely necessary, is an installation of ArcGIS Pro as well. I frequently
use this template both on my Windows tower with ArcGIS Pro, and on my MacBook Pro laptop,
so I can attest to it working in both environments. 

Admittedly, I typically start projects on my Windows machine with ArcGIS Pro. This
enables the project to initialize with a configured ArcGIS Pro project (``*.aprx`` file).
From there, I sync the project with a Git repository, and work on it in both enviroments.

Requirements
------------

Essential
++++++++++

* Conda
    * Miniconda or Anaconda
    * can be bundled with ArcGIS Pro
* Cookiecutter

It really does not matter how Conda is available, provided it is available. There are two
versions of Conda you may have, either Miniconda or Anaconda. Miniconda is the *much*
lighter weight option. Anaconda is *far* more robust. Either provides Conda, and Conda
is what Cookiecutter-Spatial-Data-Science uses for Python environment management.

If you have ArcGIS Pro installed, Miniconda is included and bundled with ArcGIS Pro. The
largest difference is you will need to access the command line from Start > ArcGIS > Python 
Command Prompt. This will ensure you have all the Conda commands available.

Optional
+++++++++

* ArcGIS Pro

Use
----

Create A Project
+++++++++++++++++

From the command line, in a folder or directory you want to create a new project, ensure the
Conda environment with Cookiecutter installed is active, and then use...

.. code-block::

  cookiecutter https://github.com/esri/cookiecutter-spatial-data-science

...to start a new project.

You will be prompted to answer a few questions for setting up the project, and once answered,
your new project will be created in its own directory. The project setup includes initializing
the project with Git and performing an initial commit enabling you to quickly get to work.


.. note::

    Once created, you normally will want to jump into this directory and continue working. If 
    not as familiar with the command line, you can move to different directories using
    the ``cd`` (change directory) command. Hence, if your project directory is named 
    ``sik-project``, you can jump into this directory using the command ``cd sik-project``.

Create Conda Environment
+++++++++++++++++++++++++

While not always enrirely necessary, it is a good practice to create a Conda enviroment for your
project. Cookiecutter-Spatial-Data-Science includes an ``environment.yml`` file with a number
of packages I typically include. My philosopy is to be rather inclusive in this file. Hence,
before creating your project I encourage you to prune this file.

Once happy with the packages included in the ``environment.yml`` file, I have streamlined the
many common tasks using the Makefile pattern. Although not idencial, I was able to mimic the
behavior on Windows in the included ``make.bat`` file. One of the very common tasks is creation
of a new Conda environment.

The command...

.. code-block::

    make env

...will create your new Conda environment. Rather than using the default location for Conda
environments, this command creates the environment right in the project in the ``./env``
directory. Especially if your projects reside on a different drive than where your Conda
installation resides, this can avoid filling up your main drive with Python pacakges for
Conda environments.

Once created, you can now use this environment using the command...

.. code-block::

    conda activate ./env
