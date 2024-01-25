import importlib.util
import logging
from pathlib import Path
from typing import Union, Optional

from .main import has_arcpy

__all__ = ['configure_logging']

if importlib.util.find_spec("pandas") is None:
    has_pandas = False
else:
    has_pandas = True
    import pandas as pd
    __all__ = __all__ + ['format_pandas_for_logging']


class ArcpyHandler(logging.Handler):
    """
    Logging message handler capable of routing logging through ArcPy AddMessage, AddWarning and AddError methods.
    DEBUG and INFO logging messages are be handled by the AddMessage method. WARNING logging messages are handled
    by the AddWarning method. ERROR and CRITICAL logging messages are handled by the AddError method.
    Basic use consists of the following.
    .. code-block:: python
        logger = logging.getLogger('arcpy-logger')
        logger.setLevel('INFO')
        ah = ArcpyHandler()
        logger.addHandler(ah)
        logger.debug('nauseatingly detailed debugging message')
        logger.info('something actually useful to know')
        logger.warning('The sky may be falling')
        logger.error('The sky is falling.)
        logger.critical('The sky appears to be falling because a giant meteor is colliding with the earth.')
    """

    # since everything goes through ArcPy methods, we do not need a message line terminator
    terminator = ''

    def __init__(self, level: Union[int, str] = 10):

        # throw logical error if arcpy not available
        if not has_arcpy:
            raise EnvironmentError('The ArcPy handler requires an environment with ArcPy, a Python environment with '
                                   'ArcGIS Pro or ArcGIS Enterprise.')

        # call the parent to cover rest of any potential setup
        super().__init__(level=level)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Args:
            record: Record containing all information needed to emit a new logging event.
        .. note::
            This method should not be called directly, but rather enables the ``Logger`` methods to
            be able to use this handler correctly.
        """
        # run through the formatter to honor logging formatter settings
        msg = self.format(record)

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
def configure_logging(
        level: Optional[Union[str, int]] = 'INFO',
        logfile_path: Union[Path, str] = None, propagate: bool = False
) -> logging.Logger:
    """
    Get Python :class:`Logger<logging.Logger>` configured to provide stream, file or, if available, ArcPy output.
    The way the method is set up, logging will be routed through ArcPy messaging using :class:`ArcpyHandler` if
    ArcPy is available. If ArcPy is *not* available, messages will be sent to the console using a
    :class:`StreamHandler<logging.StreamHandler>`. Next, if the ``logfile_path`` is provided, log messages will also
    be written to the provided path to a logfile using a :class:`FileHandler<logging.FileHandler>`.

    Valid ``log_level`` inputs include:
    * ``DEBUG`` - Detailed information, typically of interest only when diagnosing problems.
    * ``INFO`` - Confirmation that things are working as expected.
    * ``WARNING`` or ``WARN`` -  An indication that something unexpected happened, or indicative of some problem in the
            near future (e.g. ‘disk space low’). The software is still working as expected.
    * ``ERROR`` - Due to a more serious problem, the software has not been able to perform some function.
    * ``CRITICAL`` - A serious error, indicating that the program itself may be unable to continue running.

    Args:
        level: Logging level to use. Default is `'INFO'`.
        logfile_path: Where to save the logfile if file output is desired.

    .. code-block:: python

        # only output to console and potentially Pro if ArcPy is available
        configure_logging('DEBUG')
        logging.debug('nauseatingly detailed debugging message')
        logging.info('something actually useful to know')
        logging.warning('The sky may be falling')
        logging.error('The sky is falling.)
        logging.critical('The sky appears to be falling because a giant meteor is colliding with the earth.')

    """
    # ensure valid logging level
    log_str_lst = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'WARN', 'FATAL']
    log_int_lst = [0, 10, 20, 30, 40, 50]

    if not isinstance(level, (str, int)):
        raise ValueError('You must define a specific logging level for log_level as a string or integer.')
    elif isinstance(level, str) and level not in log_str_lst:
        raise ValueError(f'The log_level must be one of {log_str_lst}. You provided "{level}".')
    elif isinstance(level, int) and level not in log_int_lst:
        raise ValueError(f'If providing an integer for log_level, it must be one of the following, {log_int_lst}.')
    
    # get default logger and set logging level at the same time
    logger = logging.basicConfig(level=level)

    # configure formatting
    log_frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # if in an environment with ArcPy, add handler to bubble logging up to ArcGIS through ArcPy
    if has_arcpy:
        ah = ArcpyHandler()
        ah.setFormatter(log_frmt)
        logger.addHandler(ah)

    # create handler to console if arcpy is not providing status
    else:
        ch = logging.StreamHandler()
        ch.setFormatter(log_frmt)
        logger.addHandler(ch)

    # if a path for the logfile is provided, log results to the file
    if logfile_path is not None:

        # ensure the full path exists
        if not logfile_path.parent.exists():
            logfile_path.parent.mkdir(parents=True)

        # create and add the file handler
        fh = logging.FileHandler(str(logfile_path))
        fh.setFormatter(log_frmt)
        logger.addHandler(fh)

    # keep logging from bubbling up - keep messages just in these handlers
    logger.propagate = False

    return logger


def format_pandas_for_logging(pandas_df: pd.DataFrame, title: str, line_tab_prefix='\t\t') -> None:
    """
    Helper function facilitating outputting a :class:`Pandas DataFrame<pandas.DataFrame>` into a logfile. This function only
        formats the data frame into text for output. It should be used in conjunction with a logging method.

    .. code-block:: python

        logging.info(format_pandas_for_logging(df, title='Summary Statistics'))

    Args:
        pandas_df: Pandas ``DataFrame`` to be converted to a string and included in the logfile.
        title: String title describing the data frame.
        line_tab_prefix: Optional string comprised of tabs (``\\t\\t``) to prefix each line with providing indentation.
    """
    log_str = line_tab_prefix.join(pandas_df.to_string(index=False).splitlines(True))
    log_str = f'{title}:\n{line_tab_prefix}{log_str}'
    return log_str
