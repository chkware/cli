"""
mangle library
"""


def filename(file_name: str) -> str:
    """Mangle filepath to filename string"""

    import pathlib
    path = pathlib.Path(file_name)
    m_file = str(path.resolve())
    return m_file.lower().strip('/').replace('/', '-').replace('\\', '_').replace(':', '~')


def uniq_sha255(hashable: str) -> str:
    """Convert a string to hash"""
    import hashlib
    return hashlib.sha256(hashable.encode('utf-8')).hexdigest()
