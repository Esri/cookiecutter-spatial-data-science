import logging
import sys
from typing import Callable, Any, TypeVar
import tempfile
import shutil
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check if arcpy is available
ARCPY_AVAILABLE = 'arcpy' in sys.modules or __import__('importlib.util').util.find_spec('arcpy') is not None


def with_temp_fgdb(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    ## Temporary File Geodatabase Decorator

    This decorator function creates and manages a temporary file geodatabase that can be used to store intermediate data during geoprocessing operations.

    ### Purpose

    When performing complex geoprocessing workflows in ArcGIS/ArcPy, intermediate results often need to be stored temporarily before producing final outputs.

    This decorator:

    1. **Creates a temporary workspace** - Automatically generates a temporary file geodatabase before the decorated function executes
    2. **Provides the path** - Passes the geodatabase path to the decorated function so it can write intermediate feature classes, tables, or rasters
    3. **Handles cleanup** - Automatically deletes the temporary geodatabase and all its contents after the function completes (whether successful or not)

    ### Benefits

    - **Prevents workspace clutter** - No leftover temporary files in your project directories
    - **Automatic resource management** - No need to manually create/delete temp workspaces
    - **Exception safety** - Cleanup occurs even if the function raises an error
    - **Reusable pattern** - Can be applied to any function needing temporary storage

    ### Typical Use Case

    Useful when a geoprocessing workflow requires multiple steps where intermediate outputs from one tool become inputs to another, but those intermediate outputs 
    are not needed in the final result.

    !!! warning "When NOT to Use"

    When the itermediate data is not large enough to warrant a file geodatabase (tens of thousands of features or records, not millions), this decorator may add 
    unnecessary complexity. In those cases, consider using the `memory` workspace. This saves the data in memory (RAM), and is much faster for small to moderate 
    datasets.
    """

    # @wraps preserves the original function's metadata (name, docstring, etc.) when creating the wrapper
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        # Check if arcpy is available before proceeding, and log a warning if it's not
        if not ARCPY_AVAILABLE:
            logger.error(
                "arcpy is not available in the current environment. "
                "This script requires ArcGIS Pro or an environment with arcpy installed."
            )
            raise EnvironmentError("arcpy is required to run this function, but it is not available in the current Python environment.")
        else:
            import arcpy

        # create the temporary directory and file geodatabase
        tmp_dir = tempfile.mkdtemp()
        tmp_gdb = arcpy.management.CreateFileGDB(out_folder_path=tmp_dir, out_name='temp_data.gdb')[0]

        # use the try block to invoke the wrapped function
        try:

            # set the workspace to the temporary file geodatabase so any intermediate datasets are cleaned up
            with arcpy.EnvManager(workspace=tmp_gdb):
                return func(*args, **kwargs)

        # still raise exceptions so errors can be debugged
        except Exception:
            raise

        # clean up intermediate data, even if errors are encountered
        finally:
            arcpy.management.Delete(tmp_gdb)
            shutil.rmtree(tmp_dir, ignore_errors=True)

    return wrapper