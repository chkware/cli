# type: ignore
import json

import pytest

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.third_party.http_fetcher import ApiResponse
from chk.modules.fetch import ApiResponseDict, HttpDocument


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
