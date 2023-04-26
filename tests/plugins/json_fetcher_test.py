# type: ignore
import pytest

from chk.plugins.fetcher import ApiResponse
from chk.plugins.json_fetcher import JsonApiResponse, fetch_json


class TestJsonApiResponse:
    @staticmethod
    def test_from_api_response_pass() -> None:
        resp = ApiResponse(
            {
                "code": 200,
                "info": "HTTP/1.0 200 Ok",
                "headers": {"Accept": "application/json"},
                "body": '{"name": "value"}',
            }
        )

        api_response = JsonApiResponse.from_api_response(resp)
        assert isinstance(api_response["body"], dict)

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
            JsonApiResponse.from_api_response(resp)


class TestFetchJson:

    @staticmethod
    def test_fetch_json_pass():
        resp = fetch_json(
            {
                "url": "https://dummyjson.com/products/1",
                "method": "GET",
                "headers": {"Accept": "application/json", "Application": "pytest"},
            }
        )

        assert isinstance(resp, JsonApiResponse)

    @staticmethod
    def test_fetch_json_pass_raise_error():
        with pytest.raises(RuntimeError):
            fetch_json(
                {
                    "url": "https://httpbin.org/xml",
                    "method": "GET",
                    "headers": {"Accept": "application/xml", "Application": "pytest"},
                }
            )
