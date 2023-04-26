# type: ignore

import dataclasses

import requests
from requests.structures import CaseInsensitiveDict

from chk.infrastructure.third_party.fetcher import ApiResponse, fetch


class TestApiResponse:
    @staticmethod
    def test_from_response_pass() -> None:
        @dataclasses.dataclass
        class SampleCls:
            version: int

        cid = CaseInsensitiveDict()
        cid["Accept"] = "application/json"
        cid["Content-Type"] = "application/json"
        cid["Application"] = "internal"

        resp = requests.Response()
        resp._content = b'{"success": "ok"}'
        resp.status_code = 200
        resp.url = "https://valid.url"
        resp.raw = SampleCls(10)
        resp.reason = "Ok"
        resp.headers = cid

        api_response = ApiResponse.from_response(resp)
        assert (
            str(api_response)
            == """HTTP/1.0 200 Ok\r\n\r\nAccept: application/json\r\nContent-Type: application/json\r\nApplication: internal\r\n\r\n{"success": "ok"}"""
        )


class TestFetch:
    @staticmethod
    def test_fetch_pass():
        resp = fetch(
            {
                "url": "https://dummyjson.com/products/1",
                "method": "GET",
                "headers": {"Accept": "application/json", "Application": "pytest"},
            }
        )

        assert isinstance(resp, ApiResponse)
