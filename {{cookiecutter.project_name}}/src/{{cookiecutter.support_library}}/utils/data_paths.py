from pathlib import Path

class DataPaths(object):

    def __init__(self, data_directory) -> None:

        # ensure data directory is correctly formatted and exists
        data_dir = data_directory if isinstance(Path) else Path(data_directory)
        data_dir = data_dir.absolute()
        if not data_dir.exists():
            raise ValueError(f'The provided path to the data directory does not appear to exist - {data_dir}')

        # add all the output resources as paths
        dir_raw = dir_data/'raw'
        dir_ext = dir_data/'external'
        dir_int = dir_data/'interim'
        dir_out = dir_data/'processed'

        gdb_raw = dir_raw/'raw.gdb'
        gdb_int = dir_int/'interim.gdb'
        gdb_out = dir_out/'processed.gdb'
        gdb_ext = dir_ext/'external.gdb'


class Paths(object):

    def __init__(self, root_directory: Path) -> None:

        self.dir = root_directory
        self.gdb = root_directory.root