# cliblog
Automates blogging to a jekyll based github pages blog from the command line
as well as searching that blog.

# Configuration

Configuration is handled by `$HOME/.config/cliblog.yaml`. Current options
are

`path:` the path to the local git repo of the blog


# Usage

This is intended to be used with a github pages site and automate the
creation of posts as well as tag and category pages, previewing, committing,
and pushing new posts.

Note: To use the preview function, you must have jekyll installed and
the blog configured for local preview, the script will simply run
`bundle exec jekyll serve -w` in the blog path and then open the post
in the default browser.
