import importlib.util
import inspect
import logging
import shutil
import sys
import tempfile
from functools import wraps
from typing import Callable, Any

# Configure logging
from ._logging import get_logger
logger = get_logger(__name__, level="DEBUG")

# Check if arcpy is available
ARCPY_AVAILABLE = 'arcpy' in sys.modules or importlib.util.find_spec('arcpy') is not None


def with_temp_fgdb(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    ## Temporary File Geodatabase Decorator

    This decorator function creates and manages a temporary file geodatabase that can be used to store intermediate data during geoprocessing operations.

    ### Purpose

    When performing complex geoprocessing workflows in ArcGIS/ArcPy, intermediate results often need to be stored temporarily before producing final outputs.

    This decorator:

    1. **Creates a temporary workspace** - Automatically generates a temporary file geodatabase before the decorated function executes
    2. **Provides the path** - Sets ``arcpy.env.workspace`` to the temporary GDB via ``arcpy.EnvManager`` for the duration of the call. If the
       wrapped function declares a ``temp_fgdb`` parameter, the GDB path is also injected as that keyword argument.
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

    When the intermediate data is not large enough to warrant a file geodatabase (tens of thousands of features or records, not millions), this decorator may add 
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

        # pre-declare so finally can safely skip cleanup if creation fails
        tmp_dir = None
        tmp_gdb = None

        try:
            # create the temporary directory and file geodatabase inside the try
            # block so the finally clause can clean up even if creation raises
            tmp_dir = tempfile.mkdtemp()
            tmp_gdb = arcpy.management.CreateFileGDB(out_folder_path=tmp_dir, out_name='temp_data.gdb')[0]

            # inject tmp_gdb as temp_fgdb kwarg if the wrapped function accepts it
            sig = inspect.signature(func)
            if 'temp_fgdb' in sig.parameters:
                kwargs['temp_fgdb'] = tmp_gdb

            # set the workspace to the temporary file geodatabase so any intermediate datasets are cleaned up
            with arcpy.EnvManager(workspace=tmp_gdb):
                return func(*args, **kwargs)

        # clean up intermediate data, even if errors are encountered
        finally:
            if tmp_gdb is not None:
                try:
                    # release any lingering file locks before deletion
                    arcpy.management.ClearWorkspaceCache(tmp_gdb)
                    arcpy.management.Delete(tmp_gdb)
                except Exception as cleanup_err:
                    logger.warning(
                        "Failed to delete temporary file geodatabase '%s': %s",
                        tmp_gdb, cleanup_err,
                    )
            if tmp_dir is not None:
                shutil.rmtree(tmp_dir, ignore_errors=True)

    # Explicitly set __signature__ so documentation tools (e.g. MkDocStrings) and IDEs that
    # inspect __signature__ directly report the wrapped function's real parameter list instead
    # of falling back to (*args, **kwargs). @wraps already sets __wrapped__, which lets
    # inspect.signature() resolve the correct signature at runtime, but some tools check the
    # __signature__ attribute first and skip __wrapped__ if it is absent.
    wrapper.__signature__ = inspect.signature(func)

    return wrapper