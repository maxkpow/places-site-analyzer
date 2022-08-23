import click
from urllib.parse import urlparse
from scany.core import WebDataCapture
from scany import exporters


@click.group()
def cli():
    pass


@click.command()
@click.option('--url', default="https://avoska.ru", help='Website url to analyze.')
def run(url):
    sitename = urlparse(url).netloc

    wdc = WebDataCapture()
    result = wdc.start(website=url, timeout=3)

    exporters.to_excel(result, sitename)

cli.add_command(run)