# Cookiecutter Reference

This document provides a reference for the Cookiecutter template used in this project. It outlines the variables and 
options available for customization when generating a new project using this template.

<!--start-->
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

### Documentation layout

Files in the `./docsrc` directory are used to build the documentation. The following files are included by
default.

    mkdocs.yml                    # MkDocs configuration file. This is where navigation is set up.
    mkdocs/
        index.md                  # Documentation homepage.
        api.md                    # API (Python package) documentation generated from docstrings using MkDocStrings
        notebooks/                # Directory to put Jupyter Notebooks
        ...                       # Other markdown pages, images and files.

!!! note
    
    The structure of the documentation pages is derived directly from the way files are organized in this directory. 
    This is well explained in the [MkDocs: File Layout](https://www.mkdocs.org/user-guide/writing-your-docs/#file-layout) 
    documentation.

### Notebooks

Any Jupyter Notebooks located in `./docsrc/mkdocs/notebooks` will be converted into documentation pages able to be
included in your table of contents specified in `./docsrc/mkdocs.yml`. You will need to manually move any Jupyter
Notebooks you want included in the documentation into this directory.

!!! note

    I used to automatically copy Jupyter Notebooks from `./notebooks` into the documentation, but this created two problems.
    First, a LOT of the notebooks were copied, which were not needed in the documentation. Second, frequently I did something
    to alter the Notebook I did not really want in the documentation. 
    
    Hence, to avoid these two issues, now the template requires deliberately moving the Jupyter Notebooks you want to include 
    in the documentation from `./notebooks` to `./docsrc/mkdocs/notebooks`.


## Logging

As a best practice, it is recommended to set up logging for your application using the
`:get_logger` function. This ensures logging is properly routed to the console, logfile
and ArcPy messaging as appropriate. For example, in each module of your application, you 
should set up a logger like this:

``` python
from {{cookiecutter.support_library}}.utils import get_logger

logger = get_logger(__name__, level='DEBUG', add_stream_handler=False)
```

This ensures logging is consistent across your application and can be easily managed. Then, when
you create a script in the scripts diretory, you can configure the root logger as needed for that
script's execution context.

``` python
import datetime
from pathlib import Path

from {{cookiecutter.support_library}}.utils import get_logger

# get the path to a directory to store logfiles - assuming script is in scripts directory
script_pth = Path(__file__)
dir_prj = script_pth.parent.parent
dir_logs = dir_prj / 'data' / 'logs'

# ensure the log directory exists
if not dir_logs.exists():
    dir_logs.mkdir(parents=True)

# get the name of the scritp without the .py extension
script_name = script_pth.stem

if __name__ == "__main__":

    # define the logfile path with a timestamp - enables unique logfile per execution
    logfile_path = dir_logs / f'{script_name}_{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}.log'

    # ommitting the name uses the root logger - will output both to console and logfile
    logger = get_logger(level='INFO', add_stream_handler=True, logfile_path=logfile_path)

    # from here on out, use the logger to log messages
    logger.debug('This is a debug message, which will not be shown since the log level is set to INFO.')
    logger.info('This is an informational message, which will be shown in both the console and logfile.')
    logger.warning('This is a warning message, indicating a potential issue.')
    logger.error('This is an error message, indicating a failure in a specific operation.')
    logger.critical('This is a critical message, indicating a severe failure that may stop the program.')
```

## AGENTS.md

The `AGENTS.md` file located in the project root directory provides guidance on how to effectively use AI agents, such as ChatGPT, to assist with project development. It includes tips on prompt engineering, 
best practices for interacting with AI models, and examples of how to leverage AI to enhance productivity 
and code quality.

If you want to update this file, [GitHub's guide on writing effective AGENTS.md files](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/), is a useful concise reference for creating effective AGENTS.md files.

## Commands

Here are a few commonly used commands for efficient project configuration and use.

* `make env` - creates a Conda environment in the project directory in `./env` with resources needed for 
project development
* `make jupyter` - run Jupyter notebook with options enabling connecting from another computer on the 
same network if desired
* `make docserve` - runs live server on http://127.0.0.1:8000/ to see updates to docs in real
time. This is extremely useful when building the documentation to see how it will look.
* `make docs` - builds documentation in `./docs` from resources in `./docsrc`.
* `make data` - build data using the file `./scripts/make_data.py` using the Conda environment `./env` 
created with the command `make env`

!!! note

    These commands are defined in `./make.cmd` if you want to examine, modify or extend this capability.

## BumpVersion Cliff Notes

[Bump2Version](https://github.com/c4urself/bump2version) is preconfigured based on hints from 
[this article on Medium](https://williamhayes.medium.com/versioning-using-bumpversion-4d13c914e9b8).

If you want to...

- apply a patch, `bumpversion patch`
- update version with no breaking changes (minor version update), `bumpversion minor`
- update version with breaking changes (major version update), `bumpversion major`
- create a release (tagged in version control - Git), `bumpversion --tag release`
<!--end-->
