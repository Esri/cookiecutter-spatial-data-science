---
title: Home
---
# Cookiecutter-Spatial-Data-Science 3.2.4

This template integrates ArcGIS Pro projects and tools with Data Science workflows. Please
think of this template as a collection of best practices marrying the technologies and best
practices from both disciplines. Use what works. Remove what does not. Hopefully it can make
your life more efficient and easier.

## Getting Started

Setup and basic use are well detailed with easily copyable commands in the 
[Getting Started](getting_started.md) page.

## Origins

The Cookiecutter Spatial Data Science template arose out of a need for an experienced
geographer well versed in ArcGIS Pro and Python (myself) and a _very_ experienced data 
scientist new to Esri ([Daniel](https://www.linkedin.com/in/daniel-wilson-a274b218/)) 
to efficiently collaborate, and hand off projects to other teams.

### Challenges

Every time we were working together on a project, we had to figure out how where to 
find the needed resources such as data, code, and required additional Python packages.
We also needed a way to provide some level of documentation for each project, so we
knew what to do when revisiting it a month later, and so we could hand off projects
to other teams.

The ad-hoc approach hampered efficiency at best. In reality, it was frustratingly
cumbersome to start working on a new project, and difficult to return to a previous
project, since each one was different. Handing projects off to new teams was nearly
impossible.

### Solution

This frustration led us to begin using the 
[Cookiecutter-Data-Science v1](https://cookiecutter-data-science.drivendata.org/) 
template created and maintained by [DrivenData Labs](https://drivendata.co/). We 
immediately appreciated the data science best practices baked into the tempalte, but 
quickly ran into some challenges when trying to marry ArcGIS Pro projects with
this new structure. 

Our evolution of this paradigm to integrate ArcGIS Pro projects
into the original template, add support for Windows environments, and use
Conda for Python environment management led to the Cookiecutter-Spatial-Data-Science
template. While not identical to the Cookiecutter-Data-Science template, our 
interpretation honors the best practices of the original 
[Opinions](https://cookiecutter-data-science.drivendata.org/opinions/).

### Evolution

Since building the initial Cookiecutter-Spatial-Data-Science template in early 2019,
Daniel has moved on from Esri to co-found [SeerAI](https://www.seer.ai). I moved from 
a Solution Engineer in Business Development (sales) to a Product Engineer in Development 
creating Data Engineering workflows.

For all of the subsequent years, I have continiously relied on this template for all my
work. With best practices all baked right in, I can quickly try ideas in ArcGIS Pro, 
iterate in Jupyter, migrate to a Python package, test and debug using PyTest, and have 
it all documented with minimal effort.

While I have made this template publicly available for a long time, and kept the template
current as my practices evolve, I am now attempting to provide more resources to make
this easier to discover, understand and use.

If you encounter an issue with this template, please feel free to log an issue in the
repo. If you know how to fix it, I welcome any help you are willing to lend. This project,
after all, is not my primary responsiblty. Rather, it is me sharing the tooling I have
developed over the years to make marrying ArcGIS Pro and Data Science a little easier.
