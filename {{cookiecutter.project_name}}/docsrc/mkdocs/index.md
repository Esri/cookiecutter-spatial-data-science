---
title: {{ cookiecutter.project_title }} Home
---
# {{ cookiecutter.project_title }} 0.0.0 Documentation

This is the documentation for {{ cookiecutter.project_title }}. All the Markdown (`md`) files in
`./docs` become the documentation pages.

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
