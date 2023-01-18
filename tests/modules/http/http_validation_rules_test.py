# type: ignore
import pytest

from chk.modules.http.validation_rules import allowed_method, allowed_url


class TestAllowedMethod:
    def test_success(self):
        assert allowed_method('PUT') is True

    def test_fail(self):
        with pytest.raises(ValueError):
            assert allowed_method('POT') is True


class TestAllowedURL:
    def test_http_success(self):
        assert allowed_url('http://example.org') is True

    def test_https_success(self):
        assert allowed_url('https://example.org') is True

    def test_invalid_fail(self):
        with pytest.raises(ValueError):
            assert allowed_url('https:example.org') is True

    def test_invalid_2_fail(self):
        with pytest.raises(ValueError):
            assert allowed_url('https') is True

    def test_invalid_3_fail(self):
        with pytest.raises(ValueError):
            assert allowed_url('ftp://example.org') is True
