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

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Jump to command
GOTO %1

:: Perform data preprocessing steps contained in the make_data.py script.
:data
    ENDLOCAL & (
        CALL python src/make_data.py
        ECHO ^>^>^> Data processed.
    )
    EXIT /B

:: Make documentation using Sphinx!
:docs
    ENDLOCAL & (
        CALL conda run -p ./env sphinx-build -a -b html docsrc docs
    )
	EXIT /B

:: Create the Reveal.js slides from all the notebooks
:slides
    ENDLOCAL & (
        CAll conda run -p ./env python src/ck_tools/create_reveal_slides.py
    )
    EXIT /B

:: Build the local environment from the environment file
:env
    ENDLOCAL & (

        :: Create new environment from environment file
        CALL conda create --p ./env --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"

        :: Add more fun stuff from environment file
        CALL conda env update -p ./env -f environment.yml

        :: Activate the environment
        CALL activate ./env

        :: Install the local package in development (experimental) mode
        CALL python -m pip install -e .

    )
    EXIT /B

:: Activate the environment
:env_activate
    ENDLOCAL & CALL activate ./env
    EXIT /B

:: Remove the environment
:env_remove
	ENDLOCAL & (
		CALL conda deactivate
		CALL conda env remove -p ./env -y
	)
	EXIT /B

:: Start Jupyter Lab
:jupyter
    ENDLOCAL & CALL conda activate ./env && jupyter lab --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.token=""
    EXIT /B

:: Make the package for uploading
:build
    ENDLOCAL & (

        :: Build the pip package
        CALL python setup.py sdist

        :: Build conda package
        CALL conda build ./conda-recipe --output-folder ./conda-recipe/conda-build

    )
    EXIT /B

:build_upload
    ENDLOCAL & (

        :: Build the pip package
        CALL python setup.py sdist bdist_wheel
        CALL twine upload ./dist/*

        :: Build conda package
        CALL conda build ./conda-recipe --output-folder ./conda-recipe/conda-build
        CALL anaconda upload ./conda-recipe/conda-build/win-64/{{ cookiecutter.project_name }}*.tar.bz2

    )
    EXIT /B

:: Run all tests in module
:test
	ENDLOCAL & (
		pytest testing/
	)
	EXIT /B

EXIT /B
