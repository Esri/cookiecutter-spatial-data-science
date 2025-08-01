---
title: {{ cookiecutter.project_title }} Home
---
# {{ cookiecutter.project_title }} 0.0.0 Documentation

This is the documentation for {{ cookiecutter.project_title }}. All the Markdown (`md`) files in
`./docs/mkdocs` become the documentation pages.

## Notebooks

Any Jupyter Noteoboks located in `./docs/mkdocs/notebooks` will be converted into documentation pages able to be
included in your table of contents specified in `./docs/mkdocs.yml`. You will need to manually move any Jupyter
Notebooks you want included in the documentation into this directory.

!!! note

    I used to automatically copy Jupyter Notebooks from `./notebooks` into the documentation, but this created two problems.
    First, a LOT of the notebooks were copied, which were not needed in the documentation. Second, frequently I did something
    to alter the Notebook I did not really want in the documentation. Hence, to avoid these two issues, now the template
    requires deliberately moving the Jupyter Notebooks you want to include in the documentation from `./notebooks` to
    `./docs/mkdocs/notebooks`.

## MkDocs

Documentation is built using MkDocs with a few extensions.

- [MkDocs: Writing Your Docs](https://www.mkdocs.org/user-guide/writing-your-docs/) - this is a great place to start
  understanding how to write and structure your documentation
- [MkDocStrings: Usage](https://mkdocstrings.github.io/usage/#autodoc-syntax) - Extension creating docstrings directly
  from docstrings in the Python package built with your project. This is configured to use Google docstring conventions.
- [MkDocs-Jupyter](https://mkdocs-jupyter.danielfrg.com/) - Extension enabling inclusion of Notebooks directly in the
  documentation.
- [MkDocs-Material](https://squidfunk.github.io/mkdocs-material/) - Theme used for the documentation. Useful
  information for customizing the theme if you want.
- [Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) - How to add Notes, etc.


## Commands

* `make docs` - builds documentation in `./docs` from resources in `./docsrc`.
* `make docserve` - runs live server on http://127.0.0.1:8000/ to see updates to docs in real
  time. This is extremely useful when building the documentation to see how it will look.

## Documentation layout

Files in the `./docs` directory are used to build the documentation. The following files are included by
default.

    mkdocs.yml                    # MkDocs configuration file. This is where the navigation is set up.
    docs/
        index.md                  # Documentation homepage.
        notebook-template.ipynb   # Example Jupyter Notebook included in documentation
        api.md                    # API (Python package) documentation generated from docstrings using MkDocStrings
        ...                       # Other markdown pages, images and files.

The structure of the documentation
pages is derived directly from the way files are organized in this directory. This is well explained in the
[MkDocs: File Layout](https://www.mkdocs.org/user-guide/writing-your-docs/#file-layout) documentation.
