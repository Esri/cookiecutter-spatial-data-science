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
SET PROJECT_NAME={{cookiecutter.project_name}}
SET ENV_NAME={{cookiecutter.conda_environment_name}}
SET CONDA_PARENT=arcgispro-py3

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Jump to command
GOTO %1

:: Perform data preprocessing steps contained in the make_data.py script.
:data
    ENDLOCAL & (
        CALL activate "%ENV_NAME%"
        CALL python scripts/make_data.py
        ECHO ^>^>^> Data processed.
    )
    EXIT /B

:: Get data from Azure Blob Storage
:get_data
    ENDLOCAL & (
        IF "%2"=="-o" CALL python scripts/azure_blob.py get "%PROJECT_DIR%" -o
        IF "%2"=="" CALL python scripts/azure_blob.py get "%PROJECT_DIR%"
    )
    EXIT /B

:: Push data to Azure Blob Storage
:push_data
    ENDLOCAL & (
        IF "%2"=="-o" CALL python scripts/azure_blob.py push "%PROJECT_DIR%" -o
        IF "%2"=="" CALL python scripts/azure_blob.py push "%PROJECT_DIR%"
    )
    EXIT /B
	
:: Export the current environment
:env_export
    ENDLOCAL & (
        CALL conda env export --name "%ENV_NAME%" > environment.yml
        ECHO ^>^>^> "%PROJECT_NAME%" conda environment exported to ./environment.yml
    )
    EXIT /B
	
:: Build the local environment from the environment file
:env
    ENDLOCAL & (

        :: Run this from the ArcGIS Python Command Prompt
        :: Clone and activate the new environment
        CALL conda create --name "%ENV_NAME%" --clone "%CONDA_PARENT%"
        CALL activate "%ENV_NAME%"

        :: Install additional packages
        CALL conda env update -f environment.yml

        :: Additional steps for the map widget to work in Jupyter Lab
        CALL jupyter labextension install @jupyter-widgets/jupyterlab-manager -y
        CALL jupyter labextension install arcgis-map-ipywidget@1.7.0 -y
    )
    EXIT /B

:: Activate the environment
:env_activate
    ENDLOCAL & CALL activate "%ENV_NAME%"
    EXIT /B

:: Remove the environment
:env_remove
	ENDLOCAL & (
		CALL deactivate
		CALL conda env remove --name "%ENV_NAME%" -y
	)
	EXIT /B

:: Run all tests in module
:test
	ENDLOCAL & (
		activate "%ENV_NAME%"
		pytest
	)
	EXIT /B

EXIT /B
