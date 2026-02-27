"""
Licensing

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

A copy of the license is available in the repository's
LICENSE file.
"""

import json
import logging
from pathlib import Path
import shutil
import subprocess
import importlib.util
import zipfile

# set up logging - tying into cookiecutter logging
logger = logging.getLogger("cookiecutter.hooks.post_gen_project")
logger.setLevel(logging.DEBUG)

# see if arcpy available to accommodate non-windows environments
if importlib.util.find_spec("arcpy") is not None:
    import arcpy

    HAS_ARCPY = True
else:
    HAS_ARCPY = False

# pull in values from cookiecutter
NEW_PRJ_NAME = "{{cookiecutter.project_name}}"
NEW_PRJ_TITLE = "{{cookiecutter.project_title}}"
NEW_PRJ_DESC = "{{cookiecutter.description}}"
CREATE_GH_REPO = "{{cookiecutter.create_github_repo}}"
GITHUB_ORG = "{{cookiecutter.github_organization}}"
SUPPORT_LIB = "{{cookiecutter.support_library}}"

# project path constants
DIR_PRJ = Path.cwd()
DIR_DATA = DIR_PRJ / "data"
DIR_ARCGIS = DIR_PRJ / "arcgis"
ENV_PTH = DIR_PRJ / "env"
CONFIG_PTH = DIR_PRJ / "config" / "secrets_template.yml"


def setup_data(data_pth: Path) -> Path:
    """create all the data resources for the available environment from scratch to ensure version compatibility"""

    if not HAS_ARCPY:
        logger.warning("arcpy not available; skipping file data geodatabase creation")

    # iterate the data subdirectories
    for data_name in ["interim", "raw", "processed", "external"]:

        # ensure the data subdirectory exists
        dir_pth = data_pth / data_name
        if not dir_pth.exists():
            dir_pth.mkdir(parents=True)
            logger.info(f"Created data directory: {dir_pth}")

        # if working in an arcpy environment
        if HAS_ARCPY:

            # remove the file geodatabase if it exists and recreate it to make sure compatible with version of Pro
            fgdb_pth = dir_pth / f"{data_name}.gdb"
            if fgdb_pth.exists():
                shutil.rmtree(fgdb_pth)
            arcpy.management.CreateFileGDB(str(dir_pth), f"{data_name}.gdb")
            logger.info(f"Created file geodatabase: {fgdb_pth}")

    return data_pth


def replace_aprx_toolbox(
    aprx_path: Path, old_tbx_name: str, new_tbx_name: str
) -> None:
    """Replace the default toolbox reference inside an .aprx (zip archive) by
    modifying GISProject.json directly.

    An .aprx file is a zip archive.  The toolbox reference lives in
    ``GISProject.json`` in three places:

    1. ``defaultToolbox`` – top-level field (e.g. ``.\\cookiecutter.tbx``)
    2. A ``CIMProjectItem`` whose ``catalogPath`` points to the ``.tbx``
    3. The same item's ``name`` field

    This function rewrites those values so the project points at
    *new_tbx_name* instead of *old_tbx_name*.
    """
    # read all entries from the original archive
    with zipfile.ZipFile(aprx_path, "r") as zin:
        entries = {name: zin.read(name) for name in zin.namelist()}
        infos = {name: zin.getinfo(name) for name in zin.namelist()}

    # patch GISProject.json
    gis_project = json.loads(entries["GISProject.json"])

    # 1. update defaultToolbox
    if "defaultToolbox" in gis_project:
        gis_project["defaultToolbox"] = gis_project["defaultToolbox"].replace(
            old_tbx_name, new_tbx_name
        )

    # 2 & 3. update the matching CIMProjectItem
    for item in gis_project.get("projectItems", []):
        if item.get("itemType") == "GP" and old_tbx_name in item.get("catalogPath", ""):
            item["catalogPath"] = item["catalogPath"].replace(
                old_tbx_name, new_tbx_name
            )
            item["name"] = item["name"].replace(old_tbx_name, new_tbx_name)
            # pathHint is an absolute path baked in at creation time – update it
            # so it stays consistent, though ArcGIS Pro resolves via catalogPath.
            if "pathHint" in item:
                item["pathHint"] = item["pathHint"].replace(old_tbx_name, new_tbx_name)

    entries["GISProject.json"] = json.dumps(gis_project, ensure_ascii=False).encode(
        "utf-8"
    )

    # write back to a temp file, then replace the original
    tmp_path = aprx_path.with_suffix(".aprx.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in infos:
            zout.writestr(infos[name], entries[name])

    tmp_path.replace(aprx_path)


def add_pyt_to_aprx(aprx_path: Path, pyt_name: str) -> None:
    """Add a Python toolbox (.pyt) as a project toolbox in an .aprx file.

    Opens the .aprx zip archive and appends a ``CIMProjectItem`` entry for
    the given *.pyt* file to the ``projectItems`` list inside
    ``GISProject.json``.
    """
    # read all entries from the archive
    with zipfile.ZipFile(aprx_path, "r") as zin:
        entries = {name: zin.read(name) for name in zin.namelist()}
        infos = {name: zin.getinfo(name) for name in zin.namelist()}

    gis_project = json.loads(entries["GISProject.json"])

    # build the new project item for the .pyt
    pyt_item = {
        "type": "CIMProjectItem",
        "catalogPath": f".\\{pyt_name}",
        "itemType": "GP",
        "name": pyt_name,
    }

    # append to projectItems if not already present
    project_items = gis_project.setdefault("projectItems", [])
    already_present = any(
        item.get("catalogPath", "").endswith(pyt_name) for item in project_items
    )
    if not already_present:
        project_items.append(pyt_item)

    entries["GISProject.json"] = json.dumps(
        gis_project, ensure_ascii=False
    ).encode("utf-8")

    # write back to a temp file, then replace the original
    tmp_path = aprx_path.with_suffix(".aprx.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in infos:
            zout.writestr(infos[name], entries[name])

    tmp_path.replace(aprx_path)


def copy_aprx(
    dir_arcgis: Path,
    new_prj_name: str,
    old_prj_name: str = "cookiecutter",
    remove_originals: bool = True,
) -> Path:
    """Copy the APRX with the new name."""
    # aprx paths
    old_aprx_pth = dir_arcgis / f"{old_prj_name}.aprx"
    new_aprx_pth = dir_arcgis / f"{new_prj_name}.aprx"

    # get a project object instance to monkey with
    aprx = arcpy.mp.ArcGISProject(str(old_aprx_pth))

    # copy the original tbx with a new name if not the same name
    old_tbx_name = f"{old_prj_name}.tbx"
    new_tbx_name = f"{new_prj_name}.tbx"
    old_tbx_pth = dir_arcgis / old_tbx_name
    new_tbx_pth = dir_arcgis / new_tbx_name

    if old_tbx_name != new_tbx_name:
        shutil.copy(old_tbx_pth, new_tbx_pth)
        assert new_tbx_pth.exists()
        logger.info(f"Created toolbox: {new_tbx_pth}")

    # configure default geodatabase if not already set up
    gdb_pth = dir_arcgis.parent / "data" / "interim" / "interim.gdb"
    old_gdb_pth = Path(aprx.defaultGeodatabase)

    if old_gdb_pth != gdb_pth:
        assert gdb_pth.exists()
        aprx.defaultGeodatabase = str(gdb_pth)

        logger.info(f"Set ArcGIS Pro default geodatabase to: {gdb_pth}")

    aprx.saveACopy(str(new_aprx_pth))
    logger.info(f"Created ArcGIS Pro project: {new_aprx_pth}")

    # patch toolbox references inside the new aprx (pure Python – no arcpy needed)
    if old_tbx_name != new_tbx_name:
        replace_aprx_toolbox(new_aprx_pth, old_tbx_name, new_tbx_name)
        logger.info(f"Set ArcGIS Pro default toolbox to: {new_tbx_pth}")

    # if removing original resources
    if remove_originals:
        del aprx  # have to remove object instance to remove referenced file
        old_aprx_pth.unlink()

        logger.info(f"Removed original Cookiecutter ArcGIS Pro project: {old_aprx_pth}")

        # old_tbx_pth.unlink()

    return new_aprx_pth


def init_git_repo(prj_path: Path) -> None:
    """Initialize a git repository in the project directory."""
    try:
        subprocess.run(
            ["git", "init", "--initial-branch=main"], cwd=prj_path, check=True
        )
        subprocess.run(["git", "add", "."], cwd=prj_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "initial commit"], cwd=prj_path, check=True
        )
        logger.info("Initialized git repository and made initial commit.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to initialize git repository: {e}")


def create_github_repo(repo_name: str) -> None:
    """Create a GitHub repository using the gh CLI tool."""
    try:
        subprocess.run(
            [
                "gh",
                "repo",
                "create",
                repo_name,
                "--description",
                NEW_PRJ_DESC,
                "--public",
                "--source=.",
                "--remote=origin",
                "--push",
            ],
            check=True,
        )
        logger.info(f"Created GitHub repository: {repo_name}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to create GitHub repository: {e}")


if __name__ == "__main__":

    # add logging hander to write progress to a file
    fh = logging.FileHandler(DIR_PRJ / "post_gen_project.log", mode="w")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # ensure the data directories and geodatabases are all set up
    setup_data(DIR_DATA)

    # set up the ArcGIS Pro project if arcpy is available
    if HAS_ARCPY:
        new_aprx_pth = copy_aprx(DIR_ARCGIS, NEW_PRJ_NAME)

        # add the Python toolbox (.pyt) to the project toolboxes
        pyt_name = f"{SUPPORT_LIB}.pyt"
        add_pyt_to_aprx(new_aprx_pth, pyt_name)
        logger.info(f"Added Python toolbox to ArcGIS Pro project: {pyt_name}")

    # otherwise, remove arcgis resources
    else:
        shutil.rmtree(DIR_ARCGIS)
        logger.info("arcpy not available; removed arcgis directory.")

    # rename the secrets configuration file
    CONFIG_PTH.rename(DIR_PRJ / "config" / "secrets.yml")
    logger.info("Added secrets configuration file.")

    # initialize git
    init_git_repo(DIR_PRJ)

    # if also creating a GitHub repository, do so
    if CREATE_GH_REPO.lower() == "yes":
        repo_full_name = f"{GITHUB_ORG}/{NEW_PRJ_NAME}" if GITHUB_ORG else NEW_PRJ_NAME
        create_github_repo(repo_full_name)
    else:
        logger.info("GitHub repository not created.")

    logger.info(f'Project "{NEW_PRJ_TITLE}" created!')
