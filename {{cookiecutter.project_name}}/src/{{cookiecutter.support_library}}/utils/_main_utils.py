"""Useful utility functions for {{cookiecutter.support_library}}."""

from ._logging import get_logger

# set up module-level logger
logger = get_logger("{{cookiecutter.support_library}}.utils", level="DEBUG", add_stream_handler=False)
