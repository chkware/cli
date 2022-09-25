"""
Entities for version document specification
"""
from typing import NamedTuple

from chk.modules.version.constants import VersionConfigNode as VConst


class DefaultVersionDoc(NamedTuple):
    """ Default version doc """

    doc: dict[str, object] = {
        VConst.VERSION: None,
        VConst.EXPOSE: None
    }

    def merged(self, doc: dict) -> dict:
        """ Merge given doc with default one """
        if not doc:
            doc = {}

        return self.doc | doc
