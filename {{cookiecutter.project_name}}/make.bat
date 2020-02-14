:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: VARIABLES                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

SETLOCAL
SET PROJECT_DIR=%cd%
SET PROJECT_NAME=sik-pro
SET ENV_NAME=sik_pro
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
        CALL python src/data/make_data.py
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
