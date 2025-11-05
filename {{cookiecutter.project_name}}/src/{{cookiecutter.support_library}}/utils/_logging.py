"""
Logging utilities including an ArcPy logging handler and logger configuration function.

As a best practice, it is recommended to set up logging for your application using the
`:get_logger` function. This ensures logging is properly routed to the console, logfile
and ArcPy messaging as appropriate. For example, in each module of your application, you 
should set up a logger like this:

``` python
from {{cookiecutter.support_library}}.utils import get_logger

logger = get_logger(__name__, level='DEBUG', add_stream_handler=False)
```

This ensures logging is consistent across your application and can be easily managed. Then, when
you create a script in the scripts diretory, you can configure the root logger as needed for that
script's execution context.

``` python
import datetime
from pathlib import Path

from {{cookiecutter.support_library}}.utils import get_logger

# get the path to a directory to store logfiles - assuming script is in scripts directory
script_pth = Path(__file__)
dir_prj = script_pth.parent.parent
dir_logs = dir_prj / 'data' / 'logs'

# ensure the log directory exists
if not dir_logs.exists():
    dir_logs.mkdir(parents=True)

# get the name of the scritp without the .py extension
script_name = script_pth.stem

if __name__ == "__main__":

    # define the logfile path with a timestamp - enables unique logfile per execution
    logfile_path = dir_logs / f'{script_name}_{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}.log'

    # ommitting the name uses the root logger - will output both to console and logfile
    logger = get_logger(level='INFO', add_stream_handler=True, logfile_path=logfile_path)

    # from here on out, use the logger to log messages
    logger.debug('This is a debug message, which will not be shown since the log level is set to INFO.')
    logger.info('This is an informational message, which will be shown in both the console and logfile.')
    logger.warning('This is a warning message, indicating a potential issue.')
    logger.error('This is an error message, indicating a failure in a specific operation.')
    logger.critical('This is a critical message, indicating a severe failure that may stop the program.')
```

"""
from importlib.util import find_spec
import logging
from pathlib import Path
from typing import Union, Optional

__all__ = ["get_logger", "format_pandas_for_logging", "ArcpyHandler"]


class ArcpyHandler(logging.Handler):
    """
    Logging message handler capable of routing logging through ArcPy AddMessage, AddWarning and AddError methods.
    DEBUG and INFO logging messages are be handled by the AddMessage method. WARNING logging messages are handled
    by the AddWarning method. ERROR and CRITICAL logging messages are handled by the AddError method.
    Basic use consists of the following.
    
    ``` python
    logger = logging.getLogger('arcpy-logger')
    logger.setLevel('INFO')
    
    ah = ArcpyHandler()
    logger.addHandler(ah)

    logger.debug('nauseatingly detailed debugging message')
    logger.info('something actually useful to know')
    logger.warning('The sky may be falling - notifiying of potential issues')
    logger.error('The sky is falling - notifying of a failure in a specific operation')
    logger.critical('The sky appears to be falling because a giant meteor is colliding with the earth - severe failure that may stop the program')
    ```
    """

    # since everything goes through ArcPy methods, we do not need a message line terminator
    terminator = ""

    def __init__(self, level: Union[int, str] = 10):
        # throw logical error if arcpy not available
        if find_spec("arcpy") is None:
            raise EnvironmentError(
                "The ArcPy handler requires an environment with ArcPy, a Python environment with "
                "ArcGIS Pro or ArcGIS Enterprise."
            )

        # call the parent to cover rest of any potential setup
        super().__init__(level=level)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Args:
            record: Record containing all information needed to emit a new logging event.
        
        Note:
            This method should not be called directly, but rather enables the ``Logger`` methods to
            be able to use this handler correctly.
        """
        # run through the formatter to honor logging formatter settings
        msg = self.format(record)

        # late import to avoid issues in non-ArcPy environments
        import arcpy

        # route anything NOTSET (0), DEBUG (10) or INFO (20) through AddMessage
        if record.levelno <= 20:
            arcpy.AddMessage(msg)

        # route all WARN (30) messages through AddWarning
        elif record.levelno == 30:
            arcpy.AddWarning(msg)

        # everything else; ERROR (40), FATAL (50) and CRITICAL (50), route through AddError
        else:
            arcpy.AddError(msg)


# setup logging
def get_logger(
    logger_name: Optional[str] = None,
    level: Optional[Union[str, int]] = "INFO",
    logfile_path: Union[Path, str] = None,
    log_format: Optional[str] = "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    propagate: bool = True,
    add_stream_handler: bool = True,
    add_arcpy_handler: bool = False,
) -> logging.Logger:
    """
    Get Python :class:`Logger<logging.Logger>` configured to provide stream, file or, if available, ArcPy output.
    The way the method is set up, logging will be routed through ArcPy messaging using :class:`ArcpyHandler` if
    ArcPy is available. If ArcPy is *not* available, messages will be sent to the console using a
    :class:`StreamHandler<logging.StreamHandler>`. Next, if the `logfile_path` is provided, log messages will also
    be written to the provided path to a logfile using a :class:`FileHandler<logging.FileHandler>`.

    Valid `log_level` inputs include:
    * `DEBUG` - Detailed information, typically of interest only when diagnosing problems.
    * `INFO` - Confirmation that things are working as expected.
    * `WARNING` or ``WARN`` -  An indication that something unexpected happened, or indicative of some problem in the
        near future (e.g. "disk space low"). The software is still working as expected.
    * `ERROR` - Due to a more serious problem, the software has not been able to perform some function.
    * `CRITICAL` - A serious error, indicating that the program itself may be unable to continue running.

    !!! note

        Logging levels can be provided as strings (e.g. `'DEBUG'`), corresponding integer values or using the
        logging module constants (e.g. `logging.DEBUG`).

    Args:
        logger_name: Name of the logger. If `None`, the root logger is used.
        level: Logging level to use. Default is INFO.
        log_format: Format string for the logging messages. Default is `'%(asctime)s | %(name)s | %(levelname)s | %(message)s'`.
        propagate: If `True`, log messages are passed to the handlers of ancestor loggers. Default is `False`.
        logfile_path: Where to save the logfile if file output is desired.
        add_stream_handler: If `True`, add a `StreamHandler` to route logging to the console. Default is `True`.
        add_arcpy_handler: If `True` and ArcPy is available, add the `ArcpyHandler` to route logging through
            ArcPy messaging. Default is `False`.

    ``` python
    logger = get_logger('DEBUG')
    logger.debug('nauseatingly detailed debugging message')
    logger.info('something actually useful to know')
    logger.warning('The sky may be falling')
    logger.error('The sky is falling.')
    logger.critical('The sky appears to be falling because a giant meteor is colliding with the earth.')
    ```

    """
    # ensure valid logging level
    log_str_lst = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "WARN", "FATAL"]
    log_int_lst = [0, 10, 20, 30, 40, 50]

    if not isinstance(level, (str, int)):
        raise ValueError(
            "You must define a specific logging level for log_level as a string or integer."
        )
    elif isinstance(level, str) and level not in log_str_lst:
        raise ValueError(
            f'The log_level must be one of {log_str_lst}. You provided "{level}".'
        )
    elif isinstance(level, int) and level not in log_int_lst:
        raise ValueError(
            f"If providing an integer for log_level, it must be one of the following, {log_int_lst}."
        )

    # get default logger and set logging level at the same time
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=level)

    # clear handlers
    logger.handlers.clear()

    # configure formatting
    log_frmt = logging.Formatter(log_format)

    # set propagation
    logger.propagate = propagate

    # make sure at least a stream handler is present
    if add_stream_handler:
        # create and add the stream handler
        sh = logging.StreamHandler()
        sh.setFormatter(log_frmt)
        logger.addHandler(sh)

    # if in an environment with ArcPy, add handler to bubble logging up to ArcGIS through ArcPy
    if find_spec("arcpy") is not None and add_arcpy_handler:
        ah = ArcpyHandler()
        ah.setFormatter(log_frmt)
        logger.addHandler(ah)

    # if a path for the logfile is provided, log results to the file
    if logfile_path is not None:
        # ensure the full path exists
        if not logfile_path.parent.exists():
            logfile_path.parent.mkdir(parents=True)

        # create and add the file handler
        fh = logging.FileHandler(str(logfile_path))
        fh.setFormatter(log_frmt)
        logger.addHandler(fh)

    return logger


def format_df_for_logging(
    pandas_df: "pd.DataFrame", title: str, line_tab_prefix="\t\t"
) -> str:
    """
    Helper function facilitating outputting a Pandas DataFrame into a logfile. This function only
        formats the data frame into text for output. It should be used in conjunction with a logging method.

    ``` python
    logging.info(format_df_for_logging(df, title='Summary Statistics'))
    ```

    Args:
        pandas_df: Pandas DataFrame to be converted to a string and included in the logfile.
        title: String title describing the data frame.
        line_tab_prefix: Optional string comprised of tabs (``\\t\\t``) to prefix each line with providing indentation.
    """
    if find_spec('pandas') is None:
        raise ImportError("Pandas is required to use 'format_df_for_logging'.")
    
    # late import to avoid issues in non-Pandas environments
    import pandas as pd

    # ensure proper type
    if not isinstance(pandas_df, pd.DataFrame):
        raise TypeError("The 'pandas_df' argument must be a Pandas DataFrame.")
    
    # format the data frame to a string with each line prefixed by the provided tab prefix
    log_str = line_tab_prefix.join(pandas_df.to_string(index=False).splitlines(True))

    # add title
    log_str = f"{title}:\n{line_tab_prefix}{log_str}"

    return log_str
