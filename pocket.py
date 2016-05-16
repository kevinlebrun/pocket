#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    pocket authenticate
    pocket count [--favorites] [--archive | --unread]
    pocket add <link>...
    pocket archive <id>...
    pocket delete <id>...
    pocket take <n> [--then-delete | --then-archive] [--oldest | --random] [--attrs=<attrs>]
    pocket (-h | --help)
    pocket --version

Commands:
    authenticate      Get an access token for batch work.
    count             Count the number of items in your Pocket list.
    add               Add any links given as parameter.
    take              Take a given number of the newest unread items.

Options:
    -h --help           Show this screen.
    --version           Show version.
    --attrs=<attrs>     Coma separated attributes for an item (see Pocket API).
"""

from pocket import pocket
from docopt import docopt
import sys
import os
import prettytable

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

    if args['take']:
        attrs = args['--attrs'].split(',') if args['--attrs'] else None
        items = pocket.take(
                consumer_key,
                access_token,
                number=int(args['<n>']),
                attributes=attrs,
                oldest=args['--oldest'],
                delete=args['--then-delete'],
                archive=args['--then-archive'],
                # random=args['--random'],
                )

        if sys.stdout.isatty():
            table = prettytable.PrettyTable()
            table.field_names = items[0].keys()
            table.align = 'l'

            for item in items:
                table.add_row(item.values())

            print table
        else:
            print '\n'.join('\t'.join(item.values()) for item in items)

        return

    if args['archive']:
        pocket.archive(consumer_key, access_token, ids=args['<id>'])
        return

    if args['delete']:
        pocket.delete(consumer_key, access_token, ids=args['<id>'])
        return

    if args['add']:
        pocket.add(consumer_key, access_token, links=args['<link>'])
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
    except pocket.PocketException as e:
        print e
        sys.exit(1)

