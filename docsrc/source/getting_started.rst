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

* Conda (can be bundled with ArcGIS Pro)
* Cookiecutter

It really does not matter how Conda is available, provided it is available. There are two
versions of Conda you may have, either Miniconda or Anaconda. Miniconda is the *much*
lighter weight option. Anaconda is far more robust. Either provides Conda, and Conda
is what Cookiecutter-Spatial-Data-Science uses for Python environment management.

If you have ArcGIS Pro installed, Miniconda is included and bundled with ArcGIS Pro. The
largest difference is you will need to access the command line from Start > ArcGIS > Python 
Command Prompt. This will ensure you have all the Conda commands available.

Optional
+++++++++

* ArcGIS Pro

Use
----