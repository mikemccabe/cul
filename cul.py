#!/usr/bin/env python

import sys
import requests
import redis
import argparse


colredis = redis.StrictRedis(host='redis-current.us.archive.org', port=6377)


def get_md(id):
    r = requests.get('http://archive.org/metadata/%s' % (id))
    # print r
    # print r.status_code
    # print r.headers
    # print r.encoding
    return r.json()

def taglike_collections():
    return [ 'stream_only', 'printdisabled' ] 

def reexpand_ancestry(id,dict,flattened=None):
    if flattened is None:
        flattened = []
    if id in dict.keys():
        parents = dict[id]
        if (id not in flattened): # and (len(parents) > 0):
            flattened.append(id)
        for parent in parents:
            reexpand_ancestry(parent,dict,flattened)
    else:
        print '\tDISCONNECTED VALUE? ',id
    return flattened

def find_ancestry(id,dict=None,tags=None):
    root_item = False
    if dict is None:
        dict = {}
        root_item = True
    if tags is None:
        tags = taglike_collections()
#    print id
    md = get_md(id)
    if md and 'metadata' in md:
        if 'collection' in md['metadata']:
            c = md['metadata']['collection']
            if isinstance(c, basestring) or isinstance(c, str):
                c = [c]
        else:
            c = []
        if root_item:
            print 'On disk:\n\t', c
        # parents = [a for a in c if (a in tags) or (c.index(a) == 0)]          coding explicitly to collect cruft with index > 0
        parents = []
        crufty_ancestors = []
        for cand in c:
            if (cand in tags) or (c.index(cand) == 0):
                parents.append(cand)
            else:
                crufty_ancestors.append(cand)
        for parent in parents:
            if parent not in dict.keys():
                find_ancestry(parent,dict,tags)
        dict[id] = parents
        for cruft in crufty_ancestors:
            if cruft not in dict.keys():
                print '\tCRUFT -or- INTENTIONAL MULTIPLE: ', cruft
    else:
        print '\t(could not get md)'
    return dict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='?', default=False)
    parser.add_argument('--foo',
                        help='foo',
                        action='store_true')
    largs = parser.parse_args()
    global args
    args = largs
    if args.id is None or args.id is False or len(args.id) == 0:
        parser.print_help()
        sys.exit(0)

    dict = find_ancestry(args.id)
    print 'Dictionary representation:\n\t', dict
    
    flattened = reexpand_ancestry(args.id,dict)
    flattened.remove(args.id)
    print 'Rehydrated flat list:\n\t', flattened

    if False:
        hello = {"foo":1, "bar": 2}
        colredis.hmset("hello", hello)

        h = colredis.hgetall("hello")

        print h


if __name__ == '__main__':
    sys.exit(main())





