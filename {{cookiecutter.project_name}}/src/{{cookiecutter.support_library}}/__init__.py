__title__ = "{{ cookiecutter.project_name }}"
__version__ = "0.0.0"
__author__ = "{{ cookiecutter.author_name }}"
__license__ = "{{ cookiecutter.open_source_license }}"
__copyright__ = "Copyright 2023 by {{ cookiecutter.author_name }}"

# add specific imports below if you want to organize your code into modules, which is mostly what I do
from . import utils
from .__main__ import example_function, ExampleObject

__all__ = ["example_function", "ExampleObject", "utils"]
