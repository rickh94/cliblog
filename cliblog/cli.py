import datetime
import os
from pathlib import Path
import sys
import click
from ruamel.yaml import YAML


@click.group()
@click.pass_context
def cli(ctx):
    if not ctx.obj:
        ctx.obj = {}
    yaml = YAML()
    with open(os.path.expanduser("~/.config/cliblog.yaml")) as configfile:
        config = yaml.load(configfile)
    ctx.obj['path'] = config['path']


@cli.command()
@click.argument("title")
@click.option("-c", "--category", prompt=True)
@click.option("-t", "--tag", multiple=True)
@click.pass_context
def post(ctx, title, category, tag):
    today = datetime.datetime.today()
    filename = today.strftime("%Y-%m-%d") + '-' + '-'.join(title.split())
    for atag in tag:
        tagpage = Path(ctx.obj['path'], 'tag', atag + '.html')
        if not tagpage.exists():
            with tagpage.open('w') as tagfile:
                tagfile.write(f"---\nlayout: tag\ntag: {atag}\n---")
    categorypage = Path(ctx.obj['path'], 'category', category + '.html')
    if not categorypage.exists():
        with categorypage.open('w') as categoryfile:
            categoryfile.write("---\nlayout: category"
                               f"\ncategory: {category}\n---")
