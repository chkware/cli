import click
from yaml import safe_load
from pprint import pp


@click.command()
@click.argument('file')
def execute(file):
    click.echo(file)

    # read yml data
    with open(file, 'r') as yf:
        yaml_data = safe_load(yf)

    pp(yaml_data)
    pp(yaml_data['request']['path'])

    # make request
    fetch(yaml_data['request'])

    # process data


def fetch(request: dict):
    pass
