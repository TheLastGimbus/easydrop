import sys

import click
from loguru import logger
from opendrop import config as ad_config

from .owl import Owl

logger.remove()
logger.add(sys.stdout, format='<green>{time:HH:mm:ss}</green> <level>{message}</level>', level='TRACE')


@click.group()
@logger.catch
def main():
    pass


@main.command()
@click.option('--email')
@logger.catch
def receive(email):
    with Owl() as o:
        config = ad_config.AirDropConfig(
            airdrop_dir='~/.config/easydrop/opendrop',
            email=email
        )
        # srv = ad_server.AirDropServer(config)
        input("Press enter to stop OWL...")


if __name__ == '__main__':
    main()
