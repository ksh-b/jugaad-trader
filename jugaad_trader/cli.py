import click

from .ucli import upstox
from .zcli import zerodha

cli = click.Group(commands={
    "zerodha": zerodha,
    "upstox": upstox
})

if __name__ == "__main__":
    cli()
