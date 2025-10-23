from typing import Union
from pathlib import Path

import pandas as pd

from .utils import get_logger

# configure module logging
logger = get_logger("{{cookiecutter.support_library}}", level="DEBUG", add_stream_handler=False)


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

    ``` python
    from {{cookiecutter.support_library}} import example_function

    pth = r'C:/path/to/some/table.csv'

    df = example_function(pth)
    ```
    """
    return pd.read_csv(in_path)


class ExampleObject(object):
    """
    This is an example object, mostly to provide a template for properly
    structuring a function and docstring for both you, and also for myself,
    since I *almost always* have to look this up, and it's a *lot* easier
    for it to be already templated.
    """

    def __init__(self, *args, **kwargs) -> None:
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

        ``` python
        from {{cookiecutter.support_library}} import ExampleObject

        pth = r'C:/path/to/some/table.csv'

        df = ExampleObject.example_function(pth)
        ```
        """
        return pd.read_csv(in_path)

    @classmethod
    def example_class_method(cls) -> "ExampleObject":
        """
        Class methods prove really useful for when you need a method to
        return an instance of the parent class. Again, I usually  have to
        search for how to do this, so I also just put it in here.

        Returns:
            An instance of the class, duh!

        ``` python
        from from {{cookiecutter.support_library}} import ExampleObject

        pth = r'C:/path/to/some/table.csv'

        obj_inst = ExampleObject.example_class_method()

        df = obj_inst.example_function(pth)
        ```
        """
        return cls()
    