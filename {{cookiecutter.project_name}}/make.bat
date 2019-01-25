:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: VARIABLES                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

SETLOCAL
SET PROJECT_DIR=%cd%
SET PROJECT_NAME={{ cookiecutter.repo_name }}
SET CONDA_PARENT={{ cookiecutter.conda_parent_environment }}

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Make Dataset
GOTO $1

:data
	activate %PROJECT_NAME%
	python src/data/make_dataset.py
	ECHO ">>> Data processed."
	EXIT
	
:: Create the local environment by cloning the parent environment
:env_create
	conda create --name %PROJECT_NAME% --clone %CONDA_PARENT%
	ECHO ">>> New conda environment, %PROJECT_NAME%, created. Activate with:"
	ECHO.
	ECHO "- source activate %PROJECT_NAME%"
	ECHO.
	ECHO "- make env_activate"
	EXIT
	
:: Export the current environment
:env_export
	conda env export --name %PROJECT_NAME% > environment.yml
	ECHO ">>> %PROJECT_NAME% conda environment exported to ./environment.yml"
	EXIT 
	
:: Build the local environment from the environment file
:env_build
	conda env create -f environment.yml
	EXIT

:: Run all tests in module
:test
	activate %PROJECT_NAME%
	pytest
	EXIT


EXIT
