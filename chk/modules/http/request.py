"""
Http doc request support module
"""
from chk.modules.http.document import HttpDocument


class RequestForHttpDocument:
    """Http document request utility"""

    @staticmethod
    def create_from_dict(raw_document: dict) -> dict:
        """Creates a Http document from dictionary
        :param raw_document: full document object to parse from
        :return dictionary containing request data
        """

