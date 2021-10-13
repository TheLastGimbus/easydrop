import click
from loguru import logger

from .owl import Owl


@click.group()
@logger.catch
def main():
    pass


@main.command()
@logger.catch
def receive():
    with Owl() as o:
        input("Press enter to stop OWL...")


if __name__ == '__main__':
    main()
