import click
from .owl import Owl
import subprocess


@click.group()
def main():
    pass


@main.command()
def receive():
    click.echo("dupadecho")
    with Owl() as o:
        input("dupa")


if __name__ == '__main__':
    main()
