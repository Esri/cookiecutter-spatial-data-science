from pathlib import Path
from typing import Optional, Union

__all__ = ['DataPaths']


class DataPaths(object):
    """
    Provides dot-syntax access to the data paths.

    .. code-block:: python

        # variable to store path to the data directory in the project
        data_dir = "C:/projects/rad_project/data"

        # create the ``DataPaths`` object instance
        paths = DataPaths(data_dir)

        # create a path to a raw data resource
        address_csv = paths.raw.dir/"address.csv"

        # read the data into a Pandas data frame
        address_df = pd.read_csv(address_csv)

    """
    def __init__(self, data_directory: Optional[Union[Path, str]]) -> None:
        """
        Args:
            data_directory: Data directory location created as part of the project creation script.
        """
        # try to locate the path if not provided - depends on package being still located in project
        if data_directory is None:
            data_dir = Path(__path__).parent.parent.parent.parent/'data'

        # create Path object instance if string provided
        elif isinstance(data_directory, str):
            data_dir = Path(data_directory)

        else:
            data_dir = data_directory

        # ensure the data directory does exist
        if not data_dir.exists():
            raise ValueError(f'Cannot locate the data directory. Please provide a path where the data directory '
                             f'can be found.')

        # create full path representation
        self.dir = data_dir.absolute()

        # add path resources
        self.raw = Paths(self.dir/'raw')
        self.ext = Paths(self.dir/'external')
        self.int = Paths(self.dir/'interim')
        self.out = Paths(self.dir/'processed')

    def __repr__(self):
        """Provide representation so when displaying in Jupyter, it shows useful information."""
        return f'<DataPaths - {self.dir}>'


class Paths(object):

    def __init__(self, root_directory: Path) -> None:

        self.dir = root_directory
        self.gdb = self.dir/f'{root_directory.stem}.gdb'
