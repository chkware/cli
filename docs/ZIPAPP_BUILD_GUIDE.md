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


## Creating Zipapp using [shiv](https://shiv.readthedocs.io/en/latest/)
Shiv is a command line utility for building fully self-contained Python zipapps as outlined in PEP 441, but with all their dependencies included.
It helps us to handle all those corner cases that might cause trouble while creating zipapp.

### Installation

```bash
pip install shiv
```
### Bundling zipapp
From the terminal run following command to bundle `chkware` as zipapp.

```bash
python3 -m shiv -c chk -o chk.pyz ./cli
```

Let’s break this command down,

`python3` is the python interpreter that will be used to bundle `chkware` as zipapp.

`shiv` is the command itself.

`-c chk` specifies the `console_script` for chkware ([defined here](https://github.com/chkware/cli/blob/f21698b1242e20b6bafbb11c597b455088f94de3/setup.cfg#L73))

`-o chk.pyz` specifies the `outfile`

`./cli` specifies the folder where the project resources are stored.

## Conclusion

Zipapps are not guaranteed to be cross-compatible with different **OS** architectures. 
For example, a pyz file built on a Mac may only work on other Macs, likewise for RHEL, etc. 
This usually only applies to zipapps that have C extensions in their dependencies. 
If all your dependencies are pure python, then chances are the pyz will work on other platforms.

Zipapps created with shiv will extract themselves into `~/.shiv`, unless overridden via `SHIV_ROOT`. 
If you create many utilities with shiv, you may want to occasionally clean this directory.




