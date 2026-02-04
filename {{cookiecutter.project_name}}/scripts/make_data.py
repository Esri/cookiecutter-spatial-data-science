"""Example script to process spatial data for the project."""
# import core Python libraries
from datetime import datetime
import importlib.util
import sys

# import third-party libraries
from pathlib import Path

# path to the root of the project
dir_prj = Path(__file__).parent.parent

# if the project package is not installed in the environment, add the source directory to the system path
if importlib.util.find_spec('{{cookiecutter.support_library}}') is None:
    
    # get the relative path to where the source directory is located
    src_dir = dir_prj / 'src'

    # throw an error if the source directory cannot be located
    if not src_dir.exists():
        raise EnvironmentError('Unable to import {{cookiecutter.support_library}}.')

    # add the source directory to the paths searched when importing
    sys.path.insert(0, str(src_dir))

# import {{cookiecutter.support_library}}
import {{cookiecutter.support_library}}
from {{cookiecutter.support_library}}.utils import get_logger
from .config import LOG_LEVEL, INPUT_DATA, OUTPUT_DATA

if __name__ == '__main__':

    # get datestring for file naming yyyymmddThhmmss
    date_string = datetime.now().strftime("%Y%m%dT%H%M%S")

    # path to save log file
    log_dir = dir_prj / 'data' / 'logs'

    # ensure location to save logs exists
    if not log_dir.exists():
        log_dir.mkdir(parents=True)

    # create full path to log file
    log_name = f'{Path(__file__).stem}_{date_string}.log'
    log_file = log_dir / log_name

    # use the log level from the config to set up logging
    logger = get_logger(logger_name=f"{Path(__file__).stem}", level=LOG_LEVEL)

    ### Main processing - put your data processing code here ###
    logger.info(f'Starting {dir_prj.name} data processing.')

    logger.info(f'Using input data from: {INPUT_DATA}')
    logger.info(f'Processed data will be saved to: {OUTPUT_DATA}')

    ###EXAMPLE PROCESSING, replace with your own code ###

    # late imports - not PEP8 compliant, should be at top, but makes it easier to clean up file for your processing steps
    from arcgis.features import GeoAccessor
    import arcpy
    import pandas as pd

    # constants / parameters for processing - according to PEP8, these should be defined in config.py or toward the top of the script
    X_COLUMN = 'longitude'
    Y_COLUMN = 'latitude'
    SPATIAL_REFERENCE_WKID = 4326

    # ensure input and output paths are Path objects
    INPUT_DATA = Path(INPUT_DATA)
    OUTPUT_DATA = Path(OUTPUT_DATA)

    # ensure the input data exists
    if not INPUT_DATA.exists():
        logger.error(f'Input data not found at: {INPUT_DATA}')
        raise FileNotFoundError(f'Unable to find input data at: {INPUT_DATA}')

    # ensure file geodatabase to save data exists
    gdb_pth = OUTPUT_DATA.parent

    # flag for valid file geodatabase
    gdb_valid = False

    # check that the path exists, is a directory, and has the .gdb suffix
    if gdb_pth.exists() and gdb_pth.is_dir() and gdb_pth.suffix.lower() == ".gdb":

            # Use arcpy to confirm it's a valid workspace
            desc = arcpy.Describe(str(gdb_pth))
            gdb_valid = (desc.dataType == "Workspace") and (desc.workspaceType == "FileSystem")

    # if the file geodatabase is not valid, log an error and raise an exception
    if not gdb_valid:
        err_msg = f'Output file geodatabase is not valid at: {gdb_pth}'
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    # read the input data into a pandas DataFrame
    df = pd.read_csv(INPUT_DATA)

    # convert the DataFrame to a spatially enabled DataFrame
    sdf = GeoAccessor.from_xy(df, x_column=X_COLUMN, y_column=Y_COLUMN, sr=SPATIAL_REFERENCE_WKID)

    # save the spatially enabled DataFrame to a file geodatabase feature class
    sdf.spatial.to_featureclass(location=OUTPUT_DATA)

    logger.info(f'Successfully completed data processing for {dir_prj.name}')
