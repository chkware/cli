# type: ignore
import json

import pytest

from chk.infrastructure.third_party.http_fetcher import ApiResponse
from chk.modules.fetch import ApiResponseDict


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
