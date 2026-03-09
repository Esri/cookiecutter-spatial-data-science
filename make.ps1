<#
.SYNOPSIS
    Project task runner for cookiecutter-spatial-data-science template development.

.DESCRIPTION
    PowerShell equivalent of make.cmd / Makefile for the template project itself.

.EXAMPLE
    .\make.ps1 docs
    .\make.ps1 env

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
$CondaDir = Join-Path $PSScriptRoot "env"

#-------------------------------------------------------------------------------
# Tasks
#-------------------------------------------------------------------------------
$Tasks = [ordered]@{

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
        Desc   = "Create and configure the local conda environment"
        Action = {
            conda env create -p $CondaDir -f environment.yml
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
