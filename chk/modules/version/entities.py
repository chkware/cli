"""
Entities for version document specification
"""
from chk.modules.version.constants import VersionConfigNode as VConst

__version_document_specification = {
    VConst.VERSION: None,
    VConst.EXPOSE: None
}


def get_version_doc_spec() -> dict:
    """
    Get variable document specification
    """
    return __version_document_specification
