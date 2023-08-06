from importlib.metadata import version

__version__ = version("dls-pairstream")
del version

__all__ = ["__version__"]
