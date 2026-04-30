---
title: Origins
---

# Origins

The Cookiecutter-Spatial-Data-Science template grew out of a need for an experienced
geographer comfortable with ArcGIS Pro and Python (myself) and a *very* experienced
data scientist new to Esri ([Daniel](https://www.linkedin.com/in/daniel-wilson-a274b218/))
to collaborate efficiently — and to hand projects off to other teams.

## Challenges

Every project we worked on together meant figuring out where to put things: data, code,
the extra Python packages we built along the way. We also wanted some baseline documentation 
in each project, so we'd know what to do when revisiting it a month later, and so other teams
could pick it up.

The ad-hoc approach hampered efficiency at best. In practice it was frustratingly
cumbersome to start a new project, and difficult to return to an old one — every project
was different. Handing them off to new teams was nearly impossible.

## Solution

That frustration led us to the
[Cookiecutter-Data-Science v1](https://cookiecutter-data-science.drivendata.org/)
template by [DrivenData Labs](https://drivendata.co/). We immediately appreciated the
data science best practices baked in, but quickly ran into friction trying to marry
ArcGIS Pro projects with the new structure.

Evolving that template to integrate ArcGIS Pro projects, support Windows environments,
and manage Python environments with Conda gave us Cookiecutter-Spatial-Data-Science.
It's not identical to its parent, but our interpretation honors the original
[Opinions](https://cookiecutter-data-science.drivendata.org/opinions/).

## Evolution

Since the initial template in early 2019, Daniel has moved on from Esri to co-found
[SeerAI](https://www.seer.ai). I moved from Solution Engineer in Business Development
(sales) to Product Engineer in Development (data-engineering workflows), and most
recently to Technical Consultant in Professional Services.

In every one of those roles I've kept relying on this template. With best practices
baked in, I can quickly try ideas in ArcGIS Pro, iterate in Jupyter, migrate to a Python
package, test and debug with PyTest, and document the whole thing with minimal effort.

More recently, with the rise of AI agents, I've been experimenting with how to make
agents part of the workflow. That's where the `AGENTS.md` file in the project root
comes in, with support for adapting it to different agent paradigms at project
initialization.

I've kept this template public and current for years as my own practices evolved.
Lately I've been investing in better resources around it so it's easier to discover,
understand, and use.

If you run into an issue, please file one in the repo. If you know how to fix it, pull
requests are very welcome. This project isn't my primary responsibility — it's me
sharing the tooling I've built over the years to make marrying ArcGIS Pro and data
science a little easier.

## In Short

What started as two people trying to collaborate without losing their minds has become
the scaffolding I reach for on every project I touch. If it saves you even a fraction
of the friction it has saved us, Cookiecutter-Spatial-Data-Science has done its job.

