__title__ = "{{ cookiecutter.project_name }}"
__version__ = "0.0.0"
__author__ = "{{ cookiecutter.author_name }}"
{% if cookiecutter.open_source_license != "No license file" %}
__license__ = "{{ cookiecutter.open_source_license }}"
{% endif %}
__copyright__ = "Copyright {% now 'utc', '%Y' %} by {{ cookiecutter.author_name }}"

# add specific imports below if you want to organize your code into modules, which is mostly what I do
from . import config as config
from . import utils
from ._main import example_function, ExampleObject

__all__ = ["config", "example_function", "ExampleObject", "utils"]
