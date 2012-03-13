
# An authenticated gateway to the Mailgun api


## About

This is a proof-of-concept of an authenticated gateway to the Mailgun API. It allows a client to make requests to the Mailgun API without authenticating.


## Usage

    $ pip install -r requirements.txt
    $ tproxy mailgun.py
    $ curl -k -s http://localhost:5000/v2/domains
    [...] json output [...]

