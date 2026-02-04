:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: LICENSING                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: Copyright 2025 Esri
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
SET CONDA_DIR="%~dp0env"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Jump to command
GOTO %1

:: Make documentation using MkDocs!
:docs
    CALL conda run -p %CONDA_DIR% mkdocs build -f ./docsrc/mkdocs.yml
    GOTO end

:: MkDocs live documentation server
:docserve
    CALL conda run -p %CONDA_DIR% mkdocs serve -f ./docsrc/mkdocs.yml
    GOTO end

:: clone the arcgispro-py3 environment
:env
    CALL conda create -p ./env --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"

:: Build the local environment from the environment file
:env
    CALL conda env update -p ./env -f environment.yml
    GOTO end

:end
    EXIT /B
