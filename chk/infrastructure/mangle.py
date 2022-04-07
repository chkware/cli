"""
mangle library
"""
import pathlib


def filename(file_name: str) -> str:
    path = pathlib.Path(file_name)
    m_file = str(path.resolve())
    return m_file.lower().strip('/').replace('/', '-').replace('\\', '_').replace(':', '~')
