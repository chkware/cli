# type: ignore

import pytest

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.symbol_table import Variables
from chk.modules.fetch import HttpDocumentSupport
from chk.modules.fetch.entities import HttpDocument


class TestHttpDocument:
    @staticmethod
    def test_bool_pass():
        ctx = FileContext(
            document={
                "version": "default:http:0.7.2",
                "request": {
                    "url": "https://jsonplaceholder.typicode.com/albums/1",
                    "method": "GET",
                },
            }
        )

        doc = HttpDocumentSupport.from_file_context(ctx)

        assert doc


class TestHttpDocumentSupport:
    @staticmethod
    def test_from_file_context_pass():
        ctx = FileContext(
            document={
                "version": "default:http:0.7.2",
                "request": {
                    "url": "https://jsonplaceholder.typicode.com/albums/1",
                    "method": "GET",
                },
            }
        )

        doc = HttpDocumentSupport.from_file_context(ctx)

        assert isinstance(doc.context, tuple)
        assert isinstance(doc.version, str)
        assert isinstance(doc.request, dict)

    @staticmethod
    def test_from_file_context_fail_no_request():
        ctx = FileContext(
            document={
                "version": "default:http:0.7.2",
            }
        )

        with pytest.raises(RuntimeError):
            HttpDocumentSupport.from_file_context(ctx)

    @staticmethod
    def test_from_file_context_fail_no_version():
        ctx = FileContext(
            document={
                "request": {
                    "url": "https://jsonplaceholder.typicode.com/albums/1",
                    "method": "GET",
                },
            }
        )

        with pytest.raises(ValueError):
            HttpDocumentSupport.from_file_context(ctx)

    @staticmethod
    def test_execute_request_pass():
        ctx = FileContext(
            document={
                "version": "default:http:0.7.2",
                "request": {
                    "url": "https://jsonplaceholder.typicode.com/albums/1",
                    "method": "GET",
                },
            }
        )

        http_doc = HttpDocumentSupport.from_file_context(ctx)
        resp = HttpDocumentSupport.execute_request(http_doc)

        assert "userId" in resp.body

    @staticmethod
    def test_process_request_template_pass():
        ctx = FileContext(
            document={
                "version": "default:http:0.7.2",
                "request": {
                    "url": "https://jsonplaceholder.typicode.com/albums/1",
                    "method": "<% method %>",
                },
            }
        )

        http_doc = HttpDocumentSupport.from_file_context(ctx)
        variable_doc = Variables({"method": "GET"})

        HttpDocumentSupport.process_request_template(http_doc, variable_doc)
        assert http_doc.request["method"] == "GET"

    @staticmethod
    def test_build_schema_pass():
        x = HttpDocumentSupport.build_schema()
        assert len(x) == 4
