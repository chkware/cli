"""Commands"""
import chk.modules.http.main as http_executor
import click


# run command
@click.command('http')
@click.argument('file', nargs=-1)
def execute_http(file):
    """Command to run HTTP request config file.\r\n
    FILE: Any .chk file, that has 'version:...' string in it."""

    file = list(file).pop(0)
    http_executor.execute(file)


# root command
@click.group('chk')
def execute_root():
    """v0.2.0 | version strings: 0.7.2"""
    pass


execute_root.add_command(execute_http)  # add `http` as sub-command
