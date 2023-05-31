import importlib

__all__ = ['has_arcpy']

# provide variable indicating if arcpy is available
has_arcpy: bool = importlib.util.findspec('arcpy') is not None
