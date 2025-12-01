"""Main module for {{cookiecutter.support_library}} package."""

from typing import Union
from pathlib import Path

import pandas as pd

from .utils import get_logger

# configure module logging, the same logger as the package-level logger
logger = get_logger("{{cookiecutter.support_library}}", level="DEBUG", add_stream_handler=False)


def example_function(in_path: Union[str, Path]) -> pd.DataFrame:
    """
    This is an example function, mostly to provide a template for properly
    structuring a function and docstring for both you, and also for myself,
    since I _almost always_ have to look this up, and it's a _lot_ easier
    for it to be already templated.

    Args:
        in_path: Required path to something you really care about, or at least
            want to exploit, a _really big_ word used to simply say, _use_.

    Returns:
        A [Pandas Dataframe][pandas.dataframe].

    ``` python title= "using example_function"
    from {{cookiecutter.support_library}} import example_function

    pth = r'C:/path/to/some/table.csv'

    df = example_function(pth)
    ```
    """
    df = pd.read_csv(in_path)

    logger.debug(f"Read table with {len(df):,} records from {in_path}.")

    return df


class ExampleObject(object):
    """
    This is an example object, mostly to provide a template for properly
    structuring a function and docstring for both you, and also for myself,
    since I _almost always_ have to look this up, and it's a _lot_ easier
    for it to be already templated.
    """
    def __init__(self, *args, **kwargs) -> None:
        # initialize parent object if subclassed
        super().__init__(*args, **kwargs)

        logger.debug(f"Initialized {self.__class__.__name__} object instance.")

    @staticmethod
    def example_static_function(in_path: Union[str, Path]) -> pd.DataFrame:
        """
        This is an example function, mostly to provide a template for properly
        structuring a function and docstring for both you, and also for myself,
        since I _almost always_ have to look this up, and it's a _lot_ easier
        for it to be already templated.

        Args:
            in_path: Required path to something you really care about, or at least
                want to exploit, a _really big_ word used to simply say, _use_.

        Returns:
            A [Pandas Dataframe][pandas.dataframe].

        ``` python title= "using example_static_function"
        from {{cookiecutter.support_library}} import ExampleObject

        pth = r'C:/path/to/some/table.csv'

        df = ExampleObject.example_function(pth)
        ```
        """
        df = pd.read_csv(in_path)

        logger.debug(f"Read table with {len(df):,} records from {in_path}.")

        return df

    @classmethod
    def example_class_method(cls) -> "ExampleObject":
        """
        Class methods prove really useful for when you need a method to
        return an instance of the parent class. Again, I usually  have to
        search for how to do this, so I also just put it in here.

        Returns:
            An instance of [ExampleObject][{{cookiecutter.support_library}}.ExampleObject], duh!

        ``` python title="using ExampleObject.example_class_method" hlines="5 7"
        from {{cookiecutter.support_library}} import ExampleObject

        pth = r'C:/path/to/some/table.csv'

        obj_inst = ExampleObject.example_class_method()

        df = obj_inst.example_function(pth)
        ```
        """

        object_instance = cls()

        logger.debug(f"Created {cls.__name__} instance via class method.")

        return object_instance
    