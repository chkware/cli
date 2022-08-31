## Zipapp build process

Follow these steps to bundle `chkware` as zipapp.

- Please confirm that Python 3.10.x with [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today) is installed and setup on this machine
- Clone the repo 
    ```bash
    git clone https://github.com/chkware/cli.git ./cli
    ```
  
- Change to the directory 
    ```bash
    cd ./cli
    ```
      
- Make directory for local _virtualenv_ setup
    ```bash
    mkdir ./.venv
    ```

- Install all required packages
    ```bash
    pipenv install
    ```
  
- Install shiv for building the zipapp
    ```bash
    pipenv run pip install -U shiv
    ```
  
- Use the environment's python to build the zipapp. Refer to shiv [documentation](https://shiv.readthedocs.io/en/latest/#:~:text=let%E2%80%99s%20break%20this%20command%20down%2C) for further explanation.

    ```bash
     pipenv run python -m shiv -c chk -o chk.pyz .
    ```
`chk.pyz` is generated in the project folder.