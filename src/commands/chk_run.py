import click
from yaml import safe_load
from requests import request
from pprint import pp


@click.command()
@click.argument('file')
def execute(file):
    click.echo(file)

    # read yml data
    with open(file, 'r') as yf:
        yaml_data = safe_load(yf)

    pp(yaml_data)

    # make request
    make_request(yaml_data['request'])

    # process data


def make_request(request_data: dict):
    response = request(
        request_data['method'],
        request_data['path'],
    )

    pp(response.text)
