import sys

import click
from loguru import logger
from opendrop import config as ad_config, server as ad_server

from .owl import Owl

logger.remove()
logger.add(sys.stdout, format='<green>{time:HH:mm:ss}</green> <level>{message}</level>', level='TRACE')


@click.group()
@logger.catch
def main():
    pass


@main.command()
@click.option('--email', help="Your Email/AppleID")
@click.option('--phone', help="Your phone number")
@logger.catch
def receive(email, phone):
    with Owl() as o:
        config = ad_config.AirDropConfig(
            airdrop_dir='~/.config/easydrop/opendrop',
            email=email,
            phone=phone,
        )
        srv = ad_server.AirDropServer(config)
        srv.start_service()
        logger.info("Starting HTTPS server - press CTRL+C to stop...")
        srv.start_server()


if __name__ == '__main__':
    main()
