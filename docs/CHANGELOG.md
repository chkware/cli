All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- priliminary documentation need [#12](https://github.com/chkware/cli/issues/12)
- refactor code to make it testable [#23](https://github.com/chkware/cli/issues/23)

### Changed
- add support for request body for HEAD, OPTIONS http methods [#18](https://github.com/chkware/cli/issues/18)

## [0.1.0 pre-alpha] - 2022-01-26
### Added
- POST, PUT, PATCH null body support
- form enctype multipart/form-data support
- form enctype application/x-www-form-urlencoded support
- for OPTIONS, HEAD method sending body disabled
- http method support for GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD
- Support request structure
- Ability to read `.chk` file
