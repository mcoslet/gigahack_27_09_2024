from pathlib import Path


class PathUtils:
    _SRC = Path(__file__).resolve().parent.parent.parent
    _MAIN = _SRC / 'main'
    RESOURCES = _SRC / 'resources'
    DATA = RESOURCES / 'data'
    OUTPUT = RESOURCES / 'output_data'