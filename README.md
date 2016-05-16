# Pocket CLI

A different CLI for [Pocket](https://getpocket.com).

The tool does not provide a symmetrical Pocket API but some useful utilities
for my workflow.

This is work in progress. Only `authenticate` and `count` commands are
implemented.

## Usage

First you need to get the source.

    $ cd
    $ git clone https://github.com/kevinlebrun/pocket
    $ cd pocket
    $ mkvirtualenv pocket
    $ pip install -r requirements.txt
    $ python ./pocket.py --help

What's following is optional but recommended if for convenience.

    $ python ./pocket.py authenticate

At this point, you will need to copy the given URL, paste it into your browser,
accept the application, and type ENTER in the command line. The Pocket
access token is printed.

    $ export POCKET_ACCESS_TOKEN="paste the access token here"

You should be able to count unread items.

    $ python ./pocket.py count --unread

## License

(The MIT license)
