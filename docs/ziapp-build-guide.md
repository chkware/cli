# Bundling chkware as python Zipapp

## Creating Zipapp using [shiv](https://shiv.readthedocs.io/en/latest/)

#### Cloning chkware

```bash
git clone git@github.com:chkware/cli.git
```

#### Installing project dependencies
Navigate to the project folder and run the following command to install project
dependencies using `pipenv`
```bash
pipenv install
```

#### Activate pipenv shell

```bash
pipenv shell
```

#### Installing Shiv

```bash
pipenv install shiv
```
#### Bundling zipapp
From the terminal run following command to bundle `chkware` as zipapp. 
Refer to shiv [documentation](https://shiv.readthedocs.io/en/latest/#:~:text=let%E2%80%99s%20break%20this%20command%20down%2C) for further explanation.

```bash
shiv -c chk -o chk.pyz .
```
#### Cleaning up
Two folders named `build` and `chk.egg-info` are created by shiv while building the **zipapp**. You can remove these folders.

