:: Variables
SETLOCAL
SET CONDA_DIR="%~dp0env"

:: Jump to command
GOTO %1

:: jupyter lab
:jupyter
    CALL conda run -p %CONDA_DIR% jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.token=""
    GOTO end

:: black formatting
:black
    CALL conda run -p %CONDA_dIR% black src/ --verbose
    GOTO end

:linter
    GOTO black

:: run pytests
:tests
    CALL conda run -p %CONDA_DIR% pytest "%~dp0testing"
    GOTO end

:end
    EXIT /B