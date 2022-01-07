import click
from yaml import safe_load
from requests import request


@click.command()
@click.argument('file')
def execute(file):
    """execute command"""
    yaml_data = read_chk(file)
    response = make_request(yaml_data['request'])

    # process data
    print(response.text)


def read_chk(file_name: str) -> dict:
    """read yml data"""
    with open(file_name, 'r') as yf:
        return safe_load(yf)


def make_request(request_data: dict):
    """Make external api call"""
    response = request(
        request_data['method'],
        request_data['path'],
    )

    return response
