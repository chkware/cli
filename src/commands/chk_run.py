import click


@click.command()
@click.argument('file')
def execute(file):
    click.echo(file)
