---
title: Why Use It?
---
# Why use Cookiecutter-Spatial-Data-Science?

When hearing data analysis, data science or data engieering, typically the first thing coming to mind is the results.
This includes interesting reports, infographics, and maps. Figuring out how to derive these insightful products from 
data requires creative exploration. This exploration _must_ be unstructured and is nearly always a bit messy. Reproducing
the results of this exploratory process, however, requires exactly the opposite...organized structure with clean and
well documented code.

Trying to create structure in the middle of exploration hampers creativity necessary for discovery. Trying to untangle
and introduce structure once results have been discovered to reproduce the results can prove difficult at best, and 
sometimes is nearly impossible.

This is why you should use Cookiecutter-Spatial-Data-Science. Once familiar with the structure, you can easily follow
opionated best practices to be able to creatively explore, discover and communicate insights. The results of this
exploration can then be reproduced both by you, and by others...making your work expodentially more valuable.

## Others Will Thank You

Your projects should aim for clarity so colleagues can dive in, contribute, and trust the results. A clear, 
standardized project structure allows newcomers to quickly understand an analysis without wading through 
extensive documentation or reading every line of code. Well-organized code is often self-documenting, its structure 
provides context, making collaboration easier, learning smoother, and conclusions more trustworthy.

## You Will Thank You

If you have ever returned to a project from a few weeks, months or even years ago, you have contemplated questions
such as these.

* Do I need to intersect the states with the points before running the `make_data.py` script?
* Do I run the notebook `clean_data.py` or `evaluate_data.py` first?
* Where do the Zip Code polygons come from?
* Do I use `make_figures.py.old`, `make_figures_working.py` or `new_make_figures01.py`?

Similar questions are common, and the symptom of a disorganized project, the result of creative exploration without
the beneift of a structure providing the path to reproducable results.

This structure means you can easily return to your projects, and you have to answer fewer questions when others
use the results of your work.

## Opinions Are Not Binding

> A Foolish Consistency is the Hobgoblin of Little Minds
>
> - Ralph Waldo Emmerson and PEP8

Cookiecutter-Spatial-Data-Science is built on opinions, notably [PEP8](https://pep8.org) and the concept of analaysis 
as a DAG. The implementation of these best practices are simply opinions...opinions you do not have to follow.

If something else works beter for you, by all means, do it. For your own sake though, please do it consistently for 
all of the  aforementioned reasons above. Others will understand how to use your projects, and you will remember how 
to use your projects!