"""
Base document and utility
"""

import dataclasses

import cerberus
from pydantic import BaseModel, Field

from chk.infrastructure.file_loader import FileContext


@dataclasses.dataclass(slots=True)
class VersionedDocument:
    """
    Http document entity
    """

    context: tuple = dataclasses.field(default_factory=tuple)
    version: str = dataclasses.field(default_factory=str)


class VersionedDocumentV2(BaseModel):
    """
    versioned document entity
    """

    context: tuple = Field(default_factory=tuple)
    version: str = Field(default_factory=str)


class VersionedDocumentSupport:
    """DocumentVersionSupport"""

    @staticmethod
    def validate_with_schema(
        schema: dict, doc: VersionedDocument | VersionedDocumentV2
    ) -> bool:
        """Validate a document with given schema

        Args:
            schema: dict that holds schema
            doc: VersionedDocument A versioned document

        Returns:
            bool: True on success

        Raises:
            RuntimeError
        """

        validator = cerberus.Validator()
        file_ctx = FileContext(*doc.context)

        try:
            if not validator.validate(file_ctx.document, schema):
                raise RuntimeError(
                    f"File exception: Validation failed: {str(validator.errors)}"
                )
        except cerberus.validator.DocumentError as doc_err:
            raise RuntimeError(
                f"Document exception: `version` string not found: {str(doc_err)}"
            ) from doc_err

        return True
