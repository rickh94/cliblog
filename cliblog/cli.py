import atexit
import time

import datetime
import os
import signal
import webbrowser
from pathlib import Path
import subprocess
import click
import git
from ruamel.yaml import YAML
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError


@click.group()
@click.pass_context
def cli(ctx):
    if not ctx.obj:
        ctx.obj = {}
    yaml = YAML()
    with open(os.path.expanduser("~/.config/cliblog.yaml")) as configfile:
        config = yaml.load(configfile)
    ctx.obj['path'] = config['path']


class CEAValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Respose Required", cursor_position=0)
        if text.lower()[0] not in 'cea':
            raise ValidationError(message="Response must be [c]ommit, [e]dit, or [a]bort",
                                  cursor_position=0)


@cli.command()
@click.argument("title")
@click.option("-c", "--category", prompt=True, help="Choose a category for the blog")
@click.option("-t", "--tag", multiple=True, help="Add a tag to the post (can use multiple)")
@click.option("--preview/--no-preview", default=False, help="Preview before committing.")
@click.pass_context
def post(ctx, title, category, tag, preview):
    """Create a new post on your blog."""
    repo = git.Repo(ctx.obj['path'])
    origin = repo.remotes.origin
    origin.pull()
    today = datetime.datetime.today()
    new_post = today.strftime("%Y-%m-%d-") + '-'.join(title.split()) + '.md'
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
    if preview:
        old_pwd = os.getcwd()
        os.chdir(ctx.obj['path'])
        proc = subprocess.Popen(['bundle', 'exec', 'jekyll', 'serve'], stdout=subprocess.PIPE)
        time.sleep(3)
        atexit.register(os.kill, proc.pid, signal.SIGTERM)
        os.chdir(old_pwd)
    while True:
        subprocess.run([editor, postpath])
        if preview:
            webbrowser.open("http://localhost:4000/")
        done = prompt("You can [e]dit the post more, [c]ommit and post, or [a]bort "
                      "without committing or posting. ", validator=CEAValidator())
        if done.lower()[0] == 'c':
            break
        if done.lower()[0] == 'e':
            continue
        if done.lower()[0] == 'a':
            raise SystemExit(0)
    repo.index.add([str(postpath)])
    repo.index.commit(f"Add Post {title} with tags {tags} and category {category}")
    origin.push()
