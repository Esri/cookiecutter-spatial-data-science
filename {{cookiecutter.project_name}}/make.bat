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
SET SUPPORT_LIBRARY = {{cookiecutter.support_library}}
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
        CALL python src/make_data.py
        ECHO ^>^>^> Data processed.
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

        :: Install nodejs so it does not throw an error later
        CALL conda install -y nodejs

        :: Install additional packages
        CALL conda env update -f environment.yml

        :: Install the local package in development mode
        CALL python -m pip install -e "./src/%SUPPORT_LIBRARY%"

        :: Additional steps for the map widget to work in Jupyter Lab
        CALL jupyter labextension install @jupyter-widgets/jupyterlab-manager -y
        CALL jupyter labextension install arcgis-map-ipywidget@1.8.2 -y

        :: Set the ArcGIS Pro Python environment
        proenv "%ENV_NAME%"
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
