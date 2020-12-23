# GeoAI-Cookiecutter

GeoAI-Cookiecutter is an [opionated](https://medium.com/@stueccles/the-rise-of-opinionated-software-ca1ba0140d5b) analysis template striving to streamline and promote use of best practices for projects combining Geography and Artificial Intelligence through a logical, reasonably standardized, and flexible project structure.

[![Esri Logo][esrilogo]](https://www.esri.com/en-us/arcgis/products/spatial-analytics-data-science/overview)

GeoAI-Cookiecutter grew out of a need within the Advanced Analytics team at Esri to streamline project bootstrapping, encourage innovation, increase repeatability, encourage documentation, and encourage best practices based on [strong opinions (best practices)](#opinions).

## Why use this project structure?

Data Science and GIS are both about providing _actionable insights_. The visual results communicating actionable insights, maps, graphs and infographics are typically what first come to mind. Not surprisingly, these information products frequently get the most attention. However, these visualizations merely communicate results of complex analysis, and the path toward unearthing these insights requires creative exploration coupled with repeatability. Actionable insights for decision making requires structure not impeding creative innovation.

The best analyses are frequently the result of incredibly scattershot experimentation. This requires the ability to quickly test seemingly harebrained approaches. While most do not work, the ones that do, _this_ is where innovation happens and _genius_ is discovered. Once discovered, for the discovery to be useful, it must be repeatable.

While creativity and repeatability may initially first feel at odds, a standardized project structure used according to best practices not only facilitates creativity, but also enables repeatability. This, in turn, increases the ability to iterate more quickly, discover more insights, and generally become more productive. Not only will your own work benefit, this benefits your colleagues as well.

### Others Will Thank You

Templating tools started with web development. Pick a framework. Ember.js, Angular, Django, Rails - every single one has a project generator scaffolding out a project according to conventions and best practices. This speeds up starting a new project _and_ makes collaboration _much_ easier. Anybody else looking at the project will know where to look for resources, and since resources are logically organized, even if they are not familiar with the exact structure, can logically deduce where to find things. 

Thus, utilizing a standard template facilitates collaboration, repeatability, and confidence in your work. While applicable across disciplines, all of these become especially useful for projects part of research being submitted for peer review.

### You Will Thank You

Repeatability not only applies to your colleagues being able to repeat your work, it applies even more to the person who must repeat your work most often, _you_. Spaghetti code with multiple steps, and experimental iterations in different notebooks is impossible to decipher two weeks, two months, two years, or all too frequently, even two days later. Revisiting previous analysis in disorganized projects takes considerable time, and detracts from working on new and innovative projects. 

Disorganization is frustrating and dramatically adversely affects _your_ productivity. Good project structure encourages best practices, it makes them easy, so you can come back to your previous work easily and be productive!

### Nothing is Binding

> "A foolish consistency is the hobgoblin of little minds" — Ralph Waldo Emerson (and [PEP 8!](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds))

GeoAI-Cookiecutter is a _starting point_ for projects, but is not absolute. If details do not work, change them in your project based on your needs, _but be consistent_. After all, this is how GeoAI-Cookiecutter came into existence! [Cookiecutter Data Science](http://drivendata.github.io/cookiecutter-data-science/) is an excellent template for data science work, but did not meet all the needs for marrying Geographic and Artificial Intelligence analysis workflows. We extended and modified this template to achieve consistency addressing our additional needs.

Even within a project, if something does not work, simply follow the path that _does_ work, but do it with _consistency_. This way, for yourself and others looking at your work, your workflows and code will make sense.

> Consistency within a project is more important. Consistency within one module or function is the most important. ... However, know when to be inconsistent -- sometimes style guide recommendations just aren't applicable. When in doubt, use your best judgment. Look at other examples and decide what looks best. And don't hesitate to ask! — ([PEP 8!](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds))

Asking is important! _Learn_ from peers and colleagues.

## Getting Started

GeoAI-Cookiecutter provides a template for starting projects taking advantage of the combined capabilities of [ArcGIS Pro](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview), Esri Cloud GIS ([ArcGIS Enterprise](https://enterprise.arcgis.com/en/) or [ArcGIS Online](https://www.arcgis.com/index.html)), and the broad ecosystem of Machine Learning technologies using Python in a [Conda](https://docs.conda.io/en/latest/) environment. Although it is designed to accommodate environments _not_ including ArcGIS Pro, it then becomes little more than Cookiecutter Data Science. Consequently, it is _highly_ recommended you use GeoAI-Cookiecutter in an ArcGIS Pro Python Conda environment, which is installed with ArcGIS Pro.

#### Requirements

* ArcGIS Pro 2.7
* Conda - either Anaconda3 or miniconda
* Cookiecutter

Getting up and started with your first new environment is as easy as...

```batch
> conda create --name arcgis python=3.7
```

Next, activate this new environment.

```batch
> activate arcgis
```

Now, install `arcpy` and `arcgis`.

```batch
> conda install -c esri arcgis arcpy -y
```

Finally, install Cookiecutter.

```batch
> conda install -c conda-forge cookiecutter -y
```

Now, you have an environment ready to go!

If you are want to see this a walkthrough, well, we have that as well.

<iframe width="825" height="464" src="https://www.youtube.com/embed/ti4ge5wUqUY" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Starting a New Project

Now, once you have Cookiecutter installed in an environment, you can use the GeoAI-Cookiecutter template to quickly start a new project.

```batch
> cookiecutter https://github.com/esri/geoai-cookiecutter
```

Once you answer all the questions, the new project is now created as a new directory in the current working directory. Assuming your project name is `sik-pro`, your new Conda environment is going to be named `sik_pro`. Hence, to create this environment, run the following.

```bash
> cd sik-pro
> make env
```

This creates the environment and gets it ready for use. The following prompt will indicate this new environment is active by displaying the new environment name in parenthesis to the left of the command prompt. You are ready to get to work.

If you also want to see a video of this, here you go!

<iframe width="825" height="464" src="https://www.youtube.com/embed/_9DsxlCBQ_0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project Organization and Structure

The GeoAI-Cookiecutter template provides a structure for project resources, marrying data science directory structure with the functionality of ArcGIS Pro. This primarily means organizing the project following most of the best practices and conventions from Cookiecutter Data Science, and adapting ArcGIS Pro to easily work within this paradigm.

### Directory Structure

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
    ├── scripts            <- Put scripts to run things here.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   │   └── interim.gdb
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   │   └── processed.gdb
    │   └── raw            <- The original, immutable data dump.
    │       └── raw.gdb
    ├── docs               <- Location where all built html docs will reside.
    ├── docsrc             <- A default Sphinx project; see sphinx-doc.org for details
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    ├── notebooks          <- Jupyter notebooks. Naming convention is a 2 digits (for ordering),
    │   │                     descriptive name. e.g.: 01_exploratory_analysis.ipynb
    │   └── notebook_template.ipynb
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    ├── environment.yml    <- The requirements file for reproducing the analysis environment. This 
    │                         is generated by running `conda env export > environment.yml` or
    │                         `make env_export`.                         
    └── src                <- Source code for use in this project.
        └── {{ cookiecutter.support_library }} <- Library containing the bulk of code used in this 
                                                  project. 
```

### ArcGIS Pro Project (aprx) Configuration

While the ArcGIS Pro project is located in the `./arcgis` directory, the data is located in another directory. To make life easier, the three file geodatabases, interim.gdb, processed.gdb and raw.gdb are all already registered. Additionally, the arcgis, data, and notebooks directories are all also registered in the Pro project. This makes it easy to access useful resources from ArcGIS Pro.

![agp_catalog][agp_catalog]

## Opinions

Opinions guide best practices, but are still only opinions. However, following the best practices and conventions laid out by these opinions will go a long ways towards achieving repeatability, facilitating collaboration and increasing both your _and_ your colleagues confidence in your work. In the case of our team, these opionions embody team practices and Esri company policies.

### Autonomous Environment

The available machine learning and deep learning technologies available in Python is staggering. Fortunately, a large number of them are available simply as installable pip or conda packages. A very large part of reproducibility is being able to reproduce the environment. 

GeoAI-Cookiecutter facilitates this process by streamlining the process of creating a full functioning new Conda environment for a new project. To create a project preflighted with a few useful packages, simply ensure you are in the root of the project and type the following into the command line.

```bash
> make env
```

### Notebooks are for _Exploration_ and _Communication_

Jupyter Notebooks are for exploration, experimentation and communication. Notebooks are NOT for data production and analysis reproduction.

Notebooks have revolutionized data exploration and experimentation with code, and for this reason, are a favorite tool for exploring new ideas. For this reason, they _should_ be used frequently to explore workflows.

Notebooks are also tremendously valuable tool for highlighting analysis innovation and visualizing results dynamically. Frequently notebooks can be an integral part of communicating how analysis is accomplished and performed. However, the notebooks should succinctly highlight unique analysis aspects, _not_ show the entire beginning to end process.

### Raw Data Immutability

> Immutable _adjective_ - that cannot be changed; that will never change
> Synonym - unchangeable

Leaving original data unchanged, and building an automated data transformation pipeline dramatically streamlines repeatability. This frequently is _even_ to the extent of data format. This makes it much easier to revisit and revise results with new data as it becomes available. 

This is the explicit purpose of the `./data/raw` directory. Put your untouched raw data in this directory, and develop the pipeline to transform this data into a usable form, placing this usable data into the `./data/interim` directory.

Further, to repeat the work, the data does not _necessarily_ need to be in source control. By default, due to both this reason, and the common limitation of GitHub to store large files, the `./data` directory is excluded from synchronization with source control in the `.gitignore` file. As a supplementary option for enabling access to the data, GeoAI-Cookiecutter includes the capability to upload and download data using [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/).

### Analysis is a DAG

> A _directed acyclic graph_ (DAG) is a finite directed graph with no directed cycles.

Frequently data preparation is a time consuming process, and especially in the early stages of development, involves a lot of trial and error. For this reason each step in the data preparation process _should_ cache results to the interim data directory or file geodatabase, and following steps should check for this intermediate data. This way if intermediate data has already been created, the data preparation pipeline does not need to start over from the beginning every time. This is the structure of [SciKit Learn Transformers](https://scikit-learn.org/stable/data_transforms.html), both out of the box and custom transformers, assembled into a data transformation [Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline-chaining-estimators).

This is useful both in development of the data pipeline and even in production. During development, this enables iterative experimentation to continue moving forward. Once in production, this enables troubleshooting where the problem in the pipeline occurred as opposed to having to start the entire process over just to find the one place in the code causing the issue.

### Keep Secrets _Out_ of Version Control

Sharing your work is highly encouraged, but sharing sensitive information definitely is _not_. Almost without exception, compromising credentials or tokens granting access to company or organization resources can quickly compromise your position with the organization. Please do not do this. To protect access to information, _never_ put passwords or other sensitive information into any files synchronized with version control. GeoAI-Cookiecutter implements the convention of Cookiecutter Data Science by keeping this sensitive information in a special file excluded from version control, and provides a method of easily accessing these values from anywhere in the project.

#### Special File `.env`

The `.env` file is created by default for storing sensitive information when the project is created, but excluded from version control in the `.gitignore` file. If a project is downloaded from version control, typically GitHub, this file will be missing. It will either need to be procured through another channel, or simply manually recreated. 

By default, on project creation, the `.env` file will look similar to this.

```
AZURE_STORAGE_ACCOUNT_NAME = azureaccountname
AZURE_STORAGE_ACCOUNT_KEY = longcrypticcharacterstring
ESRI_GIS_URL = https://myorgname.maps.arcgis.com
ESRI_GIS_USERNAME = my_cloud_gis_username
ESRI_GIS_PASSWORD = R3@!!y_H@rd_T0_Gu3$$_@nd_H@rd3r_T0_R3m3mb3r_P@$$w0rd
```

#### Load Variables Using Dotenv

Among the packages included in the default `environment.yml` file is [python-dotenv](https://github.com/theskumar/python-dotenv). This package enables loading the variables so they are accessible using `os.getenv`. For instance, to be able to instantiate the GIS object, using variables stored in the `.env` file, the following can be used.

```python
from arcgis.gis import GIS
from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until found and load entries as env vars
load_dotenv(find_dotenv())

# use environment variables to instantiate the GIS object
gis = GIS(
    url=os.getenv('ESRI_GIS_URL'), 
    username=os.getenv('ESRI_GIS_USERNAME'),
    password=os.getenv('ESRI_GIS_PASSWORD')
)
```

## Thank You!

GeoAI-Cookiectutter is bulit on the shoulders of giants. It is merely an evoloution of existing work by DrivenData and Cookiecutter to suit the needs we have working at the intersection of geography and artificial intelligence. We owe a huge debt of gratitude to both.

### [DrivenData](https://www.drivendata.org)

[![drivendata][drivendata]](https://www.drivendata.org)

Huge thank you to [DrivenData](https://www.drivendata.org) for creating the outstanding [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science) template we used as the starting point for GeoAI-Cookiecutter. Cookiecutter Data Science provided the framework for initially addressing many of our team's internal collaboration challenges, and evolved into what you see here. DrivenData, we could not have done it without you! Thank you!

### [Cookiecutter](https://cookiecutter.readthedocs.io)

[![cookiecutter][cookiecutter]](https://cookiecutter.readthedocs.io)

Neither GeoAI-Cookiecutter nor Cookiecutter Data Science would be possible without the outstanding open source project Cookiecutter.

## Licensing
Copyright 2020 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

   [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

A copy of the license is available [directly from the Apache foundation](http://www.apache.org/licenses/LICENSE-2.0).

[cookiemonster]: resources/cookiemonster.jpg "Cookie Monster!"
[cookiecutter]: resources/cookiecutter.png "Cookiecutter Logo"
[drivendata]: resources/drivendata.svg "Driven Data Logo"
[esrilogo]: resources/esri_logo.png "Esri Logo"
[agp_catalog]: resources/arcgis_pro_catalog_tree.png "ArcGIS Pro Catalog Tree"
