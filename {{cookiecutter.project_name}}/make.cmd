:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: LICENSING                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: Copyright 2020 Esri
::
:: Licensed under the Apache License, Version 2.0 (the "License"); You
:: may not use this file except in compliance with the License. You may
:: obtain a copy of the License at
::
:: http://www.apache.org/licenses/LICENSE-2.0
::
:: Unless required by applicable law or agreed to in writing, software
:: distributed under the License is distributed on an "AS IS" BASIS,
:: WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
:: implied. See the License for the specific language governing
:: permissions and limitations under the License.
::
:: A copy of the license is available in the repository's
:: LICENSE file.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: VARIABLES                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

SETLOCAL
SET PROJECT_DIR=%cd%
SET PROJECT_NAME={{ cookiecutter.project_name }}
SET SUPPORT_LIBRARY = {{ cookiecutter.support_library }}
SET CONDA_DIR="%~dp0env"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Jump to command
GOTO %1

:: Perform data preprocessing steps contained in the make_data.py script.
:data
    CALL conda run -p %CONDA_DIR% python scripts/make_data.py
    GOTO end

:: Make documentation using Sphinx!
:docs
    CALL conda run -p %CONDA_DIR% sphinx-build -a -b html docsrc docs
    GOTO end

:: Build the local environment from the environment file
:env
    :: Create new environment from environment file
    CALL conda create -p %CONDA_DIR% --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
    GOTO add_dependencies

:: Add python dependencies from environment.yml to the project environment
:add_dependencies
        
    :: Add more fun stuff from environment file
    CALL conda env update -p %CONDA_DIR% -f environment.yml

    :: Install the local package in development (experimental) mode
    CALL conda run -p %CONDA_DIR% python -m pip install -e .

    GOTO end

:: Remove the environment
:remove_env
    CALL conda deactivate
    CALL conda env remove -p %CONDA_DIR% -y
	GOTO end

:: Start Jupyter Label
:jupyter
    CALL conda run -p %CONDA_DIR% python -m jupyterlab --ip=0.0.0.0 --allow-root --NotebookApp.token=""
    GOTO end

:: Make *.pyt zipped archive with requirements
:pyt_pkg
    CALL conda run -p %CONDA_DIR% python -m scripts/make_pyt_archive.py

:: Make the package for uploading
:wheel

    :: Build the pip package
    CALL conda run -p %CONDA_DIR% python -m build --wheel

    GOTO end

:: Run all tests in module
:test
	CALL conda run -p %CONDA_DIR% pytest "%~dp0testing"
	GOTO end

:: black formatting
:black
    CALL conda run -p %CONDA_dIR% black src/ --verbose
    GOTO end

:lint
    GOTO black

:linter
    GOTO black

:end
    EXIT /B
