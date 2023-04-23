"""
Base document and utility
"""
import dataclasses


@dataclasses.dataclass(slots=True)
class VersionedDocument:
    """
    Http document entity
    """

    context: tuple = dataclasses.field(default_factory=tuple)
    version: str = dataclasses.field(default_factory=str)
