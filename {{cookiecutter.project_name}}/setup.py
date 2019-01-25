from setuptools import find_packages, setup

setup(
    name='{{ cookiecutter.support_library }}',
    packages=find_packages(),
    version='0.1.0',
    description='{{ cookiecutter.description }}',
    author='{{ cookiecutter.author_name }}',
    license='{{ cookiecutter.open_source_license }}',
)
