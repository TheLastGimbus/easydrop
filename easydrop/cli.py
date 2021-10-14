import pathlib
import sys

import click
from loguru import logger
from opendrop import config as ad_config, server as ad_server

from .owl import Owl

logger.remove()
logger.add(sys.stdout, format='<green>{time:HH:mm:ss}</green> <level>{message}</level>', level='TRACE')

# TODO: Some static config (like email and phone number)
_conf_dir = pathlib.Path('~/.config/easydrop')


@click.group()
@logger.catch
def main():
    pass


@main.command()
@click.option('--interface', '-i', help="WiFi interface to use - if not specified, easydrop should guess it")
@click.option('--email', help="Your Email/AppleID")
@click.option('--phone', help="Your phone number")
@logger.catch
def receive(interface, email, phone):
    with Owl(interface=interface) as o:
        config = ad_config.AirDropConfig(
            airdrop_dir=(_conf_dir / 'opendrop'),
            email=email,
            phone=phone,
        )
        srv = ad_server.AirDropServer(config)
        logger.debug("Starting mDNS...")
        srv.start_service()
        logger.info("Starting HTTP server - press CTRL+C to stop...")
        srv.start_server()
        # TODO: Print stuff when receiving file
        # Currently, user is completely unaware that something came xD


if __name__ == '__main__':
    main()
