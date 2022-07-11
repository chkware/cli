from types import MappingProxyType

import pytest

from chk.modules.http.request_helper import HttpRequestArgCompiler


class TestHttpRequestArgCompiler:
    """Tests HttpRequestArgCompiler methods."""

    def test_add_url_and_method_valid(self):
        """Tests add_url_and_method with valid url and method."""
        request_data = {
            'url': 'https://httpbin.org/post',
            'method': 'POST'
        }
        request_arg = dict()
        HttpRequestArgCompiler.add_url_and_method(MappingProxyType(request_data), request_arg)
        assert request_arg['url'] == request_data['url']
        assert request_arg['method'] == request_data['method']

    def test_add_method_empty(self):
        """Tests add_url_and_method with valid url and an empty method."""
        request_data = {
            'url': 'https://httpbin.org/post',
        }
        request_arg = dict()
        with pytest.raises(ValueError):
            assert HttpRequestArgCompiler.add_url_and_method(MappingProxyType(request_data), request_arg) is False

    def test_add_method_invalid(self):
        """Tests add_url_and_method with valid url invalid method."""
        request_data = {
            'url': 'https://httpbin.org/post',
            'method': 'POXT'
        }
        request_arg = dict()
        with pytest.raises(ValueError):
            assert HttpRequestArgCompiler.add_url_and_method(MappingProxyType(request_data), request_arg) is False

    def test_add_url_invalid_scheme(self):
        """Tests add_url_and_method with invalid url scheme."""
        request_data = {
            'url': 'ws://httpbin.org/post',
            'method': 'POST'
        }
        request_arg = dict()
        with pytest.raises(ValueError):
            assert HttpRequestArgCompiler.add_url_and_method(MappingProxyType(request_data), request_arg) is False

    def test_add_url_empty(self):
        """Tests add_url_and_method with empty url."""
        request_data = {
            'url': '',
            'method': 'POST'
        }
        request_arg = dict()
        with pytest.raises(ValueError):
            assert HttpRequestArgCompiler.add_url_and_method(MappingProxyType(request_data), request_arg) is False

    def test_add_query_string_valid(self):
        """Tests _add_query_string with valid param."""
        request_data = {
            'url_params': {'foo': 'bar', 'two': 2}
        }
        request_arg = dict()
        HttpRequestArgCompiler.add_query_string(MappingProxyType(request_data), request_arg)
        assert request_arg['params'] == request_data['url_params']

    def test_add_query_string_invalid(self):
        """Tests _add_query_string with invalid key."""
        request_data = {
            'params': {'foo': 'bar', 'two': 2}
        }
        request_arg = dict()
        HttpRequestArgCompiler.add_query_string(MappingProxyType(request_data), request_arg)
        assert request_arg.get('params') is None

    def test_add_headers_valid(self):
        """Tests add_headers with valid."""
        request_data = {
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate'
            }
        }
        request_arg = dict()
        HttpRequestArgCompiler.add_headers(MappingProxyType(request_data), request_arg)
        assert request_arg['headers'] == request_data['headers']

    def test_add_authorization_basic_valid(self):
        """Tests add_authorization with valid basic auth header."""
        request_data = {
            'auth[basic]': {'username': 'Some_USER', 'password': 'Some-P@$$W03D'}
        }
        request_arg = dict()
        HttpRequestArgCompiler.add_authorization(MappingProxyType(request_data), request_arg)
        assert request_arg['auth'].username == request_data['auth[basic]']['username']
        assert request_arg['auth'].password == request_data['auth[basic]']['password']

    def test_add_authorization_be_valid(self):
        """Tests add_authorization with valid bearer auth header."""
        request_data = {
            'auth[bearer]': {'token': 'Some_TOKEN'}
        }
        request_arg = {
            'headers': {
                'authorization': None
            }
        }
        HttpRequestArgCompiler.add_authorization(MappingProxyType(request_data), request_arg)
        assert request_arg['headers']['authorization'] == "Bearer " + request_data['auth[bearer]']['token']

    def test_add_body_json_valid(self):
        """Tests add_body with valid JSON."""
        request_data = {
            'body[json]': {'var_1': 'val one', 'var_2': 4}
        }
        request_arg = dict()
        HttpRequestArgCompiler.add_body(MappingProxyType(request_data), request_arg)
        assert request_arg['json'] == request_data['body[json]']

    def test_add_body_text_valid(self):
        """Tests add_body with valid text/plain."""
        request_data = {
            'body[text]': 'Hello, this is a text/plain body.'
        }
        request_arg = {
            'data': None,
            'headers': {
                'content-type': None
            },
        }
        HttpRequestArgCompiler.add_body(MappingProxyType(request_data), request_arg)
        assert request_arg['data'] == request_data['body[text]']
        assert request_arg['headers']['content-type'] == 'text/plain'
