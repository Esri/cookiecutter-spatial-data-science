__title__ = '{{ cookiecutter.project_name }}'
__version__ = '0.0.0'
__author__ = '{{ cookiecutter.author_name }}'
__license__ = '{{ cookiecutter.open_source_license }}'
__copyright__ = 'Copyright 2022 by {{ cookiecutter.author_name }}'

__all__ = ['example_function', 'ExampleObject']

# add specific imports below if you want to organize your code into modules, which is mostly what I do
## from . import utils

from typing import Union
from pathlib import Path

import pandas as pd


def example_function(in_path: Union[str, Path]) -> pd.DataFrame:
    """
    This is an example function, mostly to provide a template for properly
    structuring a function and docstring for both you, and also for myself,
    since I *almost always* have to look this up, and it's a *lot* easier
    for it to be already templated.

    Args:
        in_path: Required path to something you really care about, or at least
            want to exploit, a really big word used to simply say, *use*.

    Returns:
        Hypothetically, a Pandas Dataframe. Good luck with that.

    .. code-block:: python

        from {{cookiecutter.support_library}} import example_function

        pth = r'C:/path/to/some/table.csv'

        df = example_function(pth)
    """
    return pd.read_csv(in_path)


class ExampleObject(object):
    """
    This is an example object, mostly to provide a template for properly
    structuring a function and docstring for both you, and also for myself,
    since I *almost always* have to look this up, and it's a *lot* easier
    for it to be already templated.
    """

    def __init__(self, *args, **kwargs):

        # is not applicable in all cases, but I always have to look it up, so it is here for simplicity's sake
        super().__init__(*args, **kwargs)

    @staticmethod
    def example_static_function(in_path: Union[str, Path]) -> pd.DataFrame:
        """
        This is an example function, mostly to provide a template for properly
        structuring a function and docstring for both you, and also for myself,
        since I *almost always* have to look this up, and it's a *lot* easier
        for it to be already templated.

        Args:
            in_path: Required path to something you really care about, or at least
                want to exploit, a really big word used to simply say, *use*.

        Returns:
            Hypothetically, a Pandas Dataframe. Good luck with that.

        .. code-block:: python

            from {{cookiecutter.support_library}} import ExampleObject

            pth = r'C:/path/to/some/table.csv'

            df = ExampleObject.example_function(pth)
        """
        return pd.read_csv(in_path)

    @classmethod
    def example_class_method(cls):
        """
        Class methods prove really useful for when you need a method to
        return an instance of the parent class. Again, I usually  have to
        search for how to do this, so I also just put it in here.

        Returns:
            An instance of the class, duh!

        .. code-block:: python

            from from {{cookiecutter.support_library}} import ExampleObject

            pth = r'C:/path/to/some/table.csv'

            obj_inst = ExampleObject.example_class_method()

            df = obj_inst.example_function(pth)
        """
        return cls()
