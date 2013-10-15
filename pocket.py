#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    pocket authenticate
    pocket count [--favorites] [--archive | --unread]
    pocket add <link>...
    pocket archive <id>...
    pocket delete <id>...
    pocket take <n> [--then-delete | --then-archive] [--oldest | --youngest | --random] [--attr]
    pocket (-h | --help)
    pocket --version

Commands:
    authenticate      Get an access token for batch work.
    count             Count the number of items in your Pocket list.
    add               Add any links given as parameter.
    take              Take a given number of the last added items.

Options:
    -h --help   Show this screen.
    --version   Show version.
    --attr      Coma separated attributes for an item (see Pocket API).
"""

from pocket import pocket
from docopt import docopt
import sys
import os

def run():
    args = docopt(__doc__, version='0.1.0')

    consumer_key = '19390-232d6d16259ab21ff3021298'
    access_token = get_access_token(consumer_key)

    if args['count']:
        print pocket.count(
                consumer_key,
                access_token,
                favorite=args['--favorites'],
                unread=args['--unread'],
                archive=args['--archive'],
                )
        return

    if args['authenticate']:
        print access_token
        return

    raise Exception('Not implemented yet')


def get_access_token(consumer_key):
    if os.environ.get('POCKET_ACCESS_TOKEN'):
        return os.environ.get('POCKET_ACCESS_TOKEN')

    return pocket.authenticate(consumer_key)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print e
        sys.exit(1)

