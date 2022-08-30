# Bundling chkware as python Zipapp

## Background
Setting up different python packages might be troublesome due to third party dependencies. Utilizing the idea of python 
zip application [(PEP 441)](https://peps.python.org/pep-0441/), **Zipapp** provides different methods
to package python projects as a zip application along with its dependencies. Full documentation of **Zipapp** is available 
[here](https://github.com/chkware/cli/issues/132).

## Benefits

*  Bundle python program into a single file and distribute it as a ready-to-run app to coworkers.
*  Handy way to distribute software using informal channels, such as sending it through a computer network or hosting it on an FTP server.
*  No need of installing pipx, or upgrade pip before install
*  All dependencies will be included in the **zipapp** - this will also help to remove package version dependencies.
*  Reduces network and maintenance cost on CI pipeline



