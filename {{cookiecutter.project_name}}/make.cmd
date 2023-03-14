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
    CALL python src/make_data.py
    GOTO end

:: Make documentation using Sphinx!
:docs
    CALL conda run -p %CONDA_DIR% sphinx-build -a -b html docsrc docs
    GOTO end

:: Create the Reveal.js slides from all the notebooks
:slides
    CAll conda run -p %CONDA_DIR% python src/ck_tools/create_reveal_slides.py
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

    :: Activate the environment
    GOTO activate_env

:: Activate the environment
:activate_env
    ENDLOCAL & CALL activate %CONDA_DIR%
    GOTO end

:: Remove the environment
:remove_env
    CALL conda deactivate
    CALL conda env remove -p %CONDA_DIR% -y
	GOTO end

:: Start Jupyter Lab
:jupyter
    CALL conda run -p %CONDA_DIR% jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.token=""
    GOTO end

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

:linter
    GOTO black

:end
    EXIT /B
