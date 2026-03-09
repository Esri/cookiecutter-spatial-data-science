:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: LICENSING                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: Copyright {% now 'utc', '%Y' %} Esri
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

:: Get ArcGIS Pro installation path from registry
FOR /F "tokens=2*" %%A IN ('REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\ESRI\ArcGISPro" /v InstallDir 2^>nul') DO SET ARCGIS_PRO_DIR=%%B

:: If registry query fails, fall back to default location
IF NOT DEFINED ARCGIS_PRO_DIR (
    SET ARCGIS_PRO_DIR="C:\Program Files\ArcGIS\Pro"
)

:: Set the ArcGIS Pro Python environment path
SET ARCGIS_PRO_PYTHON="%ARCGIS_PRO_DIR%\bin\Python\envs\arcgispro-py3"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Jump to command
GOTO %1

:: Perform data preprocessing steps contained in the make_data.py script.
:data
    CALL conda run -p %CONDA_DIR% python scripts/make_data.py
    GOTO end

:: Delete all compiled Python files
:clean
    FOR /R %%f IN (*.pyc *.pyo) DO DEL /Q "%%f" 2>nul
    FOR /D /R %%d IN (__pycache__) DO IF EXIST "%%d" RD /S /Q "%%d"
    GOTO end

:: Make documentation using MkDocs!
:docs
    CALL conda run -p %CONDA_DIR% mkdocs build -f ./docsrc/mkdocs.yml
    GOTO end

:: MkDocs live documentation server
:docserve
    CALL conda run -p %CONDA_DIR% mkdocs serve -f ./docsrc/mkdocs.yml
    GOTO end

:: Build the local environment from the environment file
:env
    :: Create new environment from environment file
    CALL conda create -p %CONDA_DIR% --clone %ARCGIS_PRO_PYTHON% -y
    GOTO add_dependencies

:: Add python dependencies from environment.yml to the project environment
:add_dependencies
        
    :: Add more fun stuff from environment file
    CALL conda env update -p %CONDA_DIR% -f environment.yml

    :: Install the local package in development (experimental) mode
    CALL conda run -p %CONDA_DIR% python -m pip install -e .

    GOTO end

:: Initialize SpecKit in the project
:speckit
    CALL specify init --here
    GOTO end

:: Start Jupyter Label
:jupyter
    CALL conda run -p %CONDA_DIR% python -m jupyterlab --ip=0.0.0.0 --allow-root --NotebookApp.token=""
    GOTO end

:: Make *.pyt zipped archive with requirements
:pytzip
    CALL conda run -p %CONDA_DIR% python -m scripts/make_pyt_archive.py
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

:lint
    GOTO black

:linter
    GOTO black

:end
    EXIT /B
