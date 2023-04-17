"""
Http document entity module
"""
import dataclasses

from chk.infrastructure.document import BaseDocument


@dataclasses.dataclass(slots=True)
class HttpDocument(BaseDocument):
    """Request class"""

    request: dict = dataclasses.field(default_factory=dict)
