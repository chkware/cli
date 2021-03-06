All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
Date: not-available <br>

## [0.3.2 `alpha`]
Date: 2022-06-10 <br>

**BREAKING CHANGE** variable support added. can be used as `variables` in `http` specification files.

### Added
- http spec file: define variable and use in request [#78](https://github.com/chkware/cli/issues/78)

### Changed
- nested dict data not getting sent in `body[json]` [#84](https://github.com/chkware/cli/issues/84)
- variables can't be used in `request.url` [#92](https://github.com/chkware/cli/issues/92)

## [0.2.0 `alpha`]
Date: 2022-03-31 <br>
Tracked milestone: [M.2022-03](https://github.com/chkware/cli/milestone/2)

**BREAKING CHANGE** use http files with `chk http FILE.chk`

### Added
- Improve error message on validation error [#34](https://github.com/chkware/cli/issues/34)
- Http module: load config class by version string on file [#68](https://github.com/chkware/cli/issues/68)
- Advance request spec. config file validation [#48](https://github.com/chkware/cli/issues/48)
- platform support for linux [#27](https://github.com/chkware/cli/issues/27)
- platform support for windows [#28](https://github.com/chkware/cli/issues/28)
- Figure out how to communicate with community [#19](https://github.com/chkware/cli/issues/19)
- Proof of concept for documentation [#47](https://github.com/chkware/cli/issues/47)

### Changed
- Remove `body[none]` from http file spec [#64](https://github.com/chkware/cli/issues/64)
- POST, PUT, PATCH methods must have at lease one `body[..` element [#39](https://github.com/chkware/cli/issues/39)
- Allow only one `body[..]` type in http specification file [#43](https://github.com/chkware/cli/issues/43)
- Allow only one `auth[..]` type in http specification file [#44](https://github.com/chkware/cli/issues/44)
- Architectural TLD [#4](https://github.com/chkware/cli/issues/4)
- `url:` must be valid URL (only http & https) [#49](https://github.com/chkware/cli/issues/49)
- Method should be one of allowed method [#50](https://github.com/chkware/cli/issues/50)


## [0.1.5 `pre-alpha`]  
Date: 2022-02-28 <br>
Tracked milestone: [M.2022-02](https://github.com/chkware/cli/milestone/1)

### Added
- validation for Http spec file [#29](https://github.com/chkware/cli/issues/29)
- validate request .chk file [#7](https://github.com/chkware/cli/issues/7)
- Find suitable libraries for going forward [#23](https://github.com/chkware/cli/issues/23)
- Ready for 1st pre-release [#14](https://github.com/chkware/cli/issues/14)
- preliminary documentation need [#12](https://github.com/chkware/cli/issues/12)

### Changed
- add support for request body for HEAD, OPTIONS http methods [#18](https://github.com/chkware/cli/issues/18)
- Improvement to docs for v0.1.5 [#36](https://github.com/chkware/cli/issues/36)

## [0.1.0 `pre-alpha`] 
Date: 2022-01-26

### Added
- POST, PUT, PATCH null body support
- form enctype multipart/form-data support
- form enctype application/x-www-form-urlencoded support
- for OPTIONS, HEAD method sending body disabled
- http method support for GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD
- Support request structure
- Ability to read `.chk` file
