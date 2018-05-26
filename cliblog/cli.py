import datetime
import os
from pathlib import Path
import subprocess
import click
import git
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
    repo = git.Repo(ctx.obj['path'])
    origin = repo.remotes.origin
    origin.pull()
    today = datetime.datetime.today()
    new_post = today.strftime("%Y-%m-%d") + '-' + '-'.join(title.split()) + '.md'
    for atag in tag:
        tag_page = Path(ctx.obj['path'], 'tag', atag + '.html')
        if not tag_page.exists():
            with tag_page.open('w') as tagfile:
                tagfile.write(f"---\nlayout: tag\ntag: {atag}\n---")
            repo.index.add([str(tag_page)])
    category_page = Path(ctx.obj['path'], 'category', category + '.md')
    if not category_page.exists():
        with category_page.open('w') as categoryfile:
            categoryfile.write("---\nlayout: category"
                               f"\ncategory: {category}\n---")
        repo.index.add([str(category_page)])
    postpath = Path(ctx.obj['path'], '_posts', new_post)
    tags = ' '.join(tag)
    with postpath.open('w') as postfile:
        postfile.write("---\n")
        postfile.write(f"title: {title}\n")
        postfile.write("layout: post\n")
        postfile.write(f"category: {category}\n")
        postfile.write(f"tags: {tags}\n")
        postfile.write("---\n")
    editor = os.environ['EDITOR'] or 'vim'
    subprocess.run([editor, postpath])
    repo.index.add([str(postpath)])
    repo.index.commit(f"Add Post {title} with tags {tags} and category {category}")
    origin.push()
