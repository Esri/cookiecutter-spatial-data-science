#!/bin/bash

python -m ipykernel install --user --name {{ cookiecutter.conda_environment_name }} --display-name "{{ cookiecutter.project_name }}"
