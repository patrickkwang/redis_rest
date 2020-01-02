#!/usr/bin/env python
"""Run REST interface for Redis."""
import argparse
from redis_rest.server import app

parser = argparse.ArgumentParser(description='Start REST interface for Redis.')
parser.add_argument('--host', default='0.0.0.0', type=str)
parser.add_argument('--port', default=6380, type=int)

args = parser.parse_args()

app.run(
    host=args.host,
    port=args.port,
    debug=False,
)
