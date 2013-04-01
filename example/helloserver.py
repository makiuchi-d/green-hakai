#!/usr/bin/env python
# coding: utf-8
from gevent.wsgi import WSGIServer
import gevent
import random
import urlparse
import sys

def app(env, start_response):
    gevent.sleep(random.random() * 0.1)
    if env['REQUEST_METHOD'] == 'POST':
        data = env['wsgi.input'].read()
        if env.get('CONTENT_TYPE') == 'application/x-www-form-urlencoded':
            for k, v in urlparse.parse_qsl(data):
                print "%s: %s" % (k, v)
        else:
            print data
    res = 'Hello World'
    header = [('Content-Length', str(len(res)))]

    if env['PATH_INFO'].startswith('/redirect'):
        header += [('Location', 'http://localhost:8889/Boom')]
        start_response("302 Moved Temporary", header)
    else:
        start_response("200 OK", header)
    return [res]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8889
    server = WSGIServer(('', port), app)
    server.serve_forever()
