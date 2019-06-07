import logging

import click
import uvicorn

from app import database

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}
LEVEL_CHOICES = click.Choice(LOG_LEVELS.keys())


@click.group('notes')
def cli():
    pass


@cli.command()
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Bind socket to this host.",
    show_default=True,
    envvar='APP_HOST',
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Bind socket to this port.",
    show_default=True,
    envvar='APP_PORT',
)
@click.option(
    "--workers",
    default=1,
    type=int,
    help="Number of worker processes. Not valid with --reload.",
    envvar='APP_WORKERS',
)
def serve(**kwargs):
    from app import app
    uvicorn.run(app, **kwargs)


@cli.command()
@click.option('-f', '--force', is_flag=True, help='Force drop and recreate tables')
def setup_db(force: bool):
    database.setup_db(force)
    print('Database set up successfully')


if __name__ == '__main__':
    cli()
