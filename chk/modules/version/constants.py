from typing import List


class VersionConfigNode:
    """represent the base of all kind of documents"""
    VERSION = 'version'


class VersionStrToSpecConfigMapping:
    """VersionStrToSpecConfigMapping lists all archetypes by version string"""

    data: List = ['default:http:0.7.2']
