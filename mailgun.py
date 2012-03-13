import re
import os

from http_parser.http import HttpStream, NoMoreData
from http_parser.reader import SocketReader
import socket


# Default to the sample api key provided by the Mailgun docs
MAILGUN_APIKEY = os.environ.get('MAILGUN_APIKEY', 'key-3ax6xnjp29jd6fds4gc373sgvjxteol0')


def basic_auth_headers(user, pw):
    """ Return the http headers for a Basic http authentication using `user` and `pw`. """
    import requests
    return requests.auth.HTTPBasicAuth('api', MAILGUN_APIKEY)(requests.models.Request()).headers


def rewrite_headers(parser, values=None):
    print values
    headers = parser.headers()
    if isinstance(values, dict):
        headers.update(values)

    httpver = "HTTP/%s" % ".".join(map(str, 
                parser.version()))

    new_headers = ["%s %s %s\r\n" % (parser.method(), parser.url(), 
        httpver)]

    new_headers.extend(["%s: %s\r\n" % (k, str(v)) for k, v in \
            headers.items()])

    return "".join(new_headers) + "\r\n"

def rewrite_request(req):
    try: 
        while True:
            parser = HttpStream(req)

            new_headers = rewrite_headers(parser, dict({'Host': 'api.mailgun.net'}, **basic_auth_headers('api', MAILGUN_APIKEY)))
            if new_headers is None:
                break
            req.send(new_headers)
            body = parser.body_file()
            while True:
                data = body.read(8192)
                if not data:
                    break
                req.writeall(data)
    except (socket.error, NoMoreData):
        pass

def rewrite_response(resp):
    try:
        while True:
            parser = HttpStream(resp)
            # we aren't doing anything here
            for data in parser:
                resp.writeall(data)
     
            if not parser.should_keep_alive():
                # close the connection.
                break
    except (socket.error, NoMoreData):
        pass

def proxy(data):
    return {'remote': ('api.mailgun.net', 443), 'ssl': True}
