import click
from .owl import Owl
import subprocess
from loguru import logger


@click.group()
@logger.catch
def main():
    pass


@main.command()
@logger.catch
def receive():
    raise 'fsdafsf'
    with Owl() as o:
        input("dupa")


if __name__ == '__main__':
    main()
