from pathlib import Path
from importlib.util import find_spec
import logging
from typing import Optional, Union

__all__ = ["build_data_directory", "has_arcpy", "has_pandas", "has_pyspark"]

# provide variable indicating if arcpy is available
has_arcpy: bool = find_spec("arcpy") is not None

# provide variable indicating if pandas is available
has_pandas: bool = find_spec("pandas") is not None

# provide variable indicating if PySpark is available
has_pyspark: bool = find_spec("pyspark") is not None


def build_data_directory(
    dir_path: Union[str, Path], include_fgdb: Optional[bool] = True
) -> Path:
    """
    Create a directory in the specified path, optionally with a File Geodatabse inside with the same name.

    .. note::
        If the parents for the directory path do not exist, they will automatically be created.

    Args:
        dir_path: Path where directory shall be created.
        include_fgdb: Whether to create File Geodatabase in same location with same name.

    Returns:
        Path to directory location.
    """
    # make sure working with a Path
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)

    # if already exists, leave it alone
    if dir_path.exists():
        logging.debug(f'Directory already exists, so not recreating, "{dir_path}"')

    # if does not exist, create it
    else:
        dir_path.mkdir(parents=True)
        logging.info(f'Created directory at "{dir_path}"')

    # if creating file geodatabase
    if include_fgdb and has_arcpy:
        # late import to avoid breaking in non-arcpy enrivonments
        import arcpy

        # create path to child resource as a string for arcpy
        gdb_pth = dir_path / f"{dir_path.stem}.gdb"

        # if already exists, do not touch
        if arcpy.Exists(str(gdb_pth)):
            logging.debug(
                f'File Geodatabase already exists, so not recreating, "{gdb_pth}"'
            )

        # if needing to create, build it
        else:
            arcpy.management.CreateFileGDB(
                out_folder_path=str(dir_path), out_name=str(gdb_pth.name)
            )

    return dir_path


def build_data_resources(data_dir: Union[str, Path]) -> Path:
    """
    Build out standard data directory structure in location where data shall reside for the project.

    Args:
        data_dir: Path to where data directory resides.

    Returns:
        Path to data directory.
    """
    # make sure working with a Path
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)

    # build the parent data directory
    build_data_directory(data_dir, include_fgdb=False)

    # build the four directories for the different types of data
    build_data_directory(data_dir / "external", False)
    build_data_directory(data_dir / "raw", False)
    build_data_directory(data_dir / "interim", True)
    build_data_directory(data_dir / "processed", True)

    return data_dir
