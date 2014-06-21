#!/usr/bin/env python

import sys
import requests
import redis




def get_md(id):
    r = requests.get('http://archive.org/metadata/%s' % (id))
    # print r
    # print r.status_code
    # print r.headers
    # print r.encoding
    return r.json()


def find_ancestry(id):
    print id
    md = get_md(id)
    if md:
        if 'metadata' not in md:
            print 'no meta', id
            return
        meta = md['metadata']
        if 'collection' not in meta:
            print 'no collection', id
            return
        c = md['metadata']['collection']
        print id, c
        if isinstance(c, basestring) or isinstance(c, str):
            c = [c]
        for pc in c:
            find_ancestry(pc)



# >>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# >>> r.status_code
# 200
# >>> r.headers['content-type']
# 'application/json; charset=utf8'
# >>> r.encoding
# 'utf-8'
# >>> r.text
# u'{"type":"User"...'
# >>> r.json()
# {u'private_gists': 419, u'total_private_repos': 77, ...}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='?', default=False)
    parser.add_argument('--foo',
                        help='foo',
                        action='store_true')
    parser.add_argument('--compare-old',
                        help='compare with old version of doc',
                        action='store_true')
    largs = parser.parse_args()
    global args
    args = largs
    if args.id is None or args.id is False or len(args.id) == 0:
        parser.print_help()
        sys.exit(0)

    find_ancestry(args.id)

    print


if __name__ == '__main__':
    sys.exit(main())





