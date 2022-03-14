"""Commands"""
import chk.modules.http.main as http_executor
import click


# run command
@click.command('http')
@click.argument('file')
def execute_http(file): http_executor.execute(file)


# root command
@click.group('chk')
def execute_root(): pass


execute_root.add_command(execute_http)  # add `http` as sub-command
