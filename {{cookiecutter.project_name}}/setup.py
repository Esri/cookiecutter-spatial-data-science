from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='{{ cookiecutter.support_library }}',
    package_dir={"": "src"},
    packages=find_packages('src'),
    version='0.1.0',
    description='{{ cookiecutter.description }}',
    long_description=long_description,
    author='{{ cookiecutter.author_name }}',
    license='{{ cookiecutter.open_source_license }}',
)