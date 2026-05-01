"""Create a zipped archive of a Python toolbox and its dependencies."""
import importlib
import inspect
from pathlib import Path
import re
import tomllib
import zipfile

# helper function to discover and add Python packages to a zipfile
def add_package(
    package_name: str, zip_file: zipfile.ZipFile, path_prefix: str = "src"
) -> None:
    """
    Add a package by name to the zipped archive.

    Args:
        package_name: Name of the Python package available in the *current* environment, but not part of a standard
             Python environment.
        zip_file: Zip file archive to add the package to.
        path_prefix: Path prefix where packages will be saved in the zip archive. By default, this is ``./src``.
    """
    # get the package
    pkg = importlib.import_module(package_name)

    # get the location where the package is saved
    pkg_pth = Path(inspect.getfile(pkg)).parent.absolute()

    # add all the resources into the zip file
    for file_path in pkg_pth.parent.glob("**/*"):
        # make sure only adding the current package - not the most efficient, but works
        if package_name in file_path.parts and "__pycache__" not in file_path.parts:
            # get the relative path so is put in the correct location in the archive
            zip_pth = path_prefix / file_path.relative_to(pkg_pth.parent)

            # write the package to the zip archive
            zip_file.write(file_path, arcname=zip_pth)


def get_package_requirements(pyproject_path: Path) -> list[str]:
    """Read runtime dependency names from pyproject.toml [project.dependencies]."""
    with open(pyproject_path, "rb") as fh:
        data = tomllib.load(fh)

    dep_lst: list[str] = data.get("project", {}).get("dependencies", [])

    # extract just the package name (strip version specifiers)
    pkg_lst = [re.match(r'~?([\d\w_-]*)[<>]?=?(\d*\.?)?', dep) for dep in dep_lst]

    return [pkg.group(1) for pkg in pkg_lst if pkg is not None]


if __name__ == "__main__":
    # get the path to the project directory
    dir_prj = Path(__file__).parent.parent.absolute()

    # get path to the *.pyt toolbox resources needed, the toolbox and the xml files with the inline documentation
    arcgis_dir = (dir_prj / "arcgis").absolute()
    pyt_lst = list(arcgis_dir.glob("*.pyt.xml"))
    pyt = list(arcgis_dir.glob("*.pyt"))[0]
    pyt_lst.append(pyt)

    # location and name to save zipfile
    zip_pth = dir_prj / f"{dir_prj.stem}.zip"

    # list of requirements from the package definition
    req_lst = get_package_requirements(dir_prj / "pyproject.toml")

    # create the zipfile
    with zipfile.ZipFile(zip_pth, "w", zipfile.ZIP_DEFLATED) as zip:
        # make the source directory to put packages
        zip.mkdir("src")

        # add requirements
        for pkg_req in req_lst:
            add_package(pkg_req, zip)

        # add the pyt resources so the toolbox is included with all the documentation
        for file_path in pyt_lst:
            zip.write(file_path, arcname=file_path.name)

    with zipfile.ZipFile(dir_prj / zip_pth, "r") as zip:
        zip.printdir()
