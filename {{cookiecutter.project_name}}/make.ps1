<#
.SYNOPSIS
    Project task runner for {{ cookiecutter.project_name }}.

.DESCRIPTION
    PowerShell equivalent of make.cmd / Makefile for project automation tasks
    including data processing, environment management, documentation, and testing.

.EXAMPLE
    .\make.ps1 env
    .\make.ps1 data
    .\make.ps1 docs

.NOTES
    Copyright 2025 Esri

    Licensed under the Apache License, Version 2.0 (the "License"); You
    may not use this file except in compliance with the License. You may
    obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied. See the License for the specific language governing
    permissions and limitations under the License.

    A copy of the license is available in the repository's LICENSE file.
#>
param(
    [Parameter(Position = 0)]
    [string]$Target = "help"
)

$ErrorActionPreference = "Stop"

#-------------------------------------------------------------------------------
# Variables
#-------------------------------------------------------------------------------
$ProjectDir    = $PSScriptRoot
$ProjectName   = "{{ cookiecutter.project_name }}"
$SupportLib    = "{{ cookiecutter.support_library }}"
$CondaDir      = Join-Path $ProjectDir "env"

# Get ArcGIS Pro installation path from the registry, fall back to default
$regKey = "HKLM:\SOFTWARE\ESRI\ArcGISPro"
if (Test-Path $regKey) {
    $ArcGISProDir = (Get-ItemProperty -Path $regKey -Name InstallDir -ErrorAction SilentlyContinue).InstallDir
}
if (-not $ArcGISProDir) {
    $ArcGISProDir = "C:\Program Files\ArcGIS\Pro"
}
$ArcGISProPython = Join-Path $ArcGISProDir "bin\Python\envs\arcgispro-py3"

#-------------------------------------------------------------------------------
# Tasks
#-------------------------------------------------------------------------------
$Tasks = [ordered]@{

    data = @{
        Desc   = "Run data preprocessing (scripts/make_data.py)"
        Action = {
            conda run -p $CondaDir python scripts/make_data.py
        }
    }

    clean = @{
        Desc   = "Delete all compiled Python files"
        Action = {
            Get-ChildItem -Path $ProjectDir -Recurse -Include *.pyc, *.pyo -File -ErrorAction SilentlyContinue |
                Remove-Item -Force
            Get-ChildItem -Path $ProjectDir -Recurse -Directory -Filter __pycache__ -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force
            Write-Host "Cleaned compiled Python files."
        }
    }

    docs = @{
        Desc   = "Build documentation using MkDocs"
        Action = {
            conda run -p $CondaDir mkdocs build -f ./docsrc/mkdocs.yml
        }
    }

    docserve = @{
        Desc   = "Start MkDocs live documentation server"
        Action = {
            conda run -p $CondaDir mkdocs serve -f ./docsrc/mkdocs.yml
        }
    }

    env = @{
        Desc   = "Clone ArcGIS Pro Python env and install dependencies"
        Action = {
            # Clone the ArcGIS Pro conda environment
            conda create -p $CondaDir --clone $ArcGISProPython -y

            # Layer on project-specific dependencies
            conda env update -p $CondaDir -f environment.yml

            # Install the local package in development mode
            conda run -p $CondaDir python -m pip install -e .
        }
    }

    add_dependencies = @{
        Desc   = "Add dependencies from environment.yml and install local package"
        Action = {
            conda env update -p $CondaDir -f environment.yml
            conda run -p $CondaDir python -m pip install -e .
        }
    }

    speckit = @{
        Desc   = "Initialize SpecKit in the project"
        Action = {
            specify init --here
        }
    }

    jupyter = @{
        Desc   = "Start JupyterLab server"
        Action = {
            conda run -p $CondaDir python -m jupyterlab --ip=0.0.0.0 --allow-root --NotebookApp.token=""
        }
    }

    test = @{
        Desc   = "Run all tests with pytest"
        Action = {
            conda run -p $CondaDir python -m pytest
        }
    }

    pytzip = @{
        Desc   = "Create *.pyt zipped archive with requirements"
        Action = {
            conda run -p $CondaDir python -m scripts/make_pyt_archive.py
        }
    }

}

#-------------------------------------------------------------------------------
# Dispatcher
#-------------------------------------------------------------------------------
if ($Target -eq "help") {
    Write-Host "`nAvailable targets:`n" -ForegroundColor Cyan
    $Tasks.GetEnumerator() | ForEach-Object {
        Write-Host ("  {0,-20} {1}" -f $_.Key, $_.Value.Desc)
    }
    Write-Host ""
} elseif ($Tasks.Contains($Target)) {
    & $Tasks[$Target].Action
} else {
    Write-Warning "Unknown target: $Target"
    & $PSCommandPath help
}
