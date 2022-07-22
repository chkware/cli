from typing import List


class VersionConfigNode:
    """represent the base of all kind of documents"""
    VERSION = 'version'


class VersionStore:
    """VersionStore lists all version strings."""

    request_versions: List = ['default:http:0.7.2']
