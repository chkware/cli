"""
Validation module for http
"""
HTTP_DOC_SCHEMA = """"""


class HttpDocumentValidation:
    """Validation handler for http documents"""

    @staticmethod
    def validate(document: dict) -> bool:
        return isinstance(document, dict)

    @staticmethod
    def validate_or_fail(document: dict) -> None:
        if HttpDocumentValidation.validate(document) is False:
            raise RuntimeError("Http document validation fail.")
