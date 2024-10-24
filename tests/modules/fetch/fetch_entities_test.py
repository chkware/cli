# type: ignore
import json

import pytest

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.symbol_table import Variables
from chk.modules.fetch import (
    ApiResponse,
    ApiResponseDict,
    HttpDocument,
    HttpDocumentSupport,
)


class TestApiResponseDict:
    @staticmethod
    def test_from_api_response_pass() -> None:
        resp = ApiResponse(
            {
                "code": 200,
                "info": "HTTP/1.0 200 Ok",
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                "body": '{"name": "value"}',
            }
        )

        api_response = ApiResponseDict.from_api_response(resp)
        assert isinstance(api_response["body_as_dict"], dict)

    @staticmethod
    def test_from_api_response_fail() -> None:
        resp = ApiResponse(
            {
                "code": 200,
                "info": "HTTP/1.0 200 Ok",
                "headers": {"Accept": "application/text"},
                "body": "some string",
            }
        )

        with pytest.raises(RuntimeError):
            ApiResponseDict.from_api_response(resp)

    @staticmethod
    def test_as_json_pass() -> None:
        resp = ApiResponse(
            {
                "code": 200,
                "info": "HTTP/1.0 200 Ok",
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                "body": '{"name": "value"}',
            }
        )

        ad = ApiResponseDict.from_api_response(resp)
        assert isinstance(ad.as_json, str)

        ad_dict = json.loads(ad.as_json)
        assert "code" in ad_dict
        assert "info" in ad_dict
        assert "headers" in ad_dict
        assert "body" in ad_dict


class TestHttpDocument:
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

        doc = HttpDocument.from_file_context(ctx)

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
            HttpDocument.from_file_context(ctx)

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

        with pytest.raises(RuntimeError):
            HttpDocument.from_file_context(ctx)


class TestHttpDocumentSupport:
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

        http_doc = HttpDocument.from_file_context(ctx)
        resp = ApiResponseDict.from_api_response(
            HttpDocumentSupport.execute_request(http_doc)
        )

        assert "userId" in resp["body_as_dict"]

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

        http_doc = HttpDocument.from_file_context(ctx)
        variable_doc = Variables({"method": "GET"})

        HttpDocumentSupport.process_request_template(http_doc, variable_doc)
        assert http_doc.request["method"] == "GET"

    @staticmethod
    def test_build_schema_pass():
        x = HttpDocumentSupport.build_schema()
        assert len(x) == 4
