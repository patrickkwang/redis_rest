"""Sanic REST interface for Redis."""
import json
import os

import aioredis
from sanic import Sanic, response

from redis_rest.apidocs import bp as apidocs_blueprint

app = Sanic()
app.config.ACCESS_LOG = False
app.blueprint(apidocs_blueprint)

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)


async def startup_connection(app, loop):
    """Start up Redis connection."""
    app.redis_connection = await aioredis.create_redis_pool(
        f'redis://{redis_host}:{redis_port}')


async def shutdown_connection(app, loop):
    """Shut down Redis connection."""
    app.redis_connection.close()
    await app.redis_connection.wait_closed()


@app.route('/get')
async def get_handler(request):
    """Get value(s) for key(s).

    Use GET for single key, MGET for multiple.
    """
    if isinstance(request.args['key'], list):
        values = await app.redis_connection.mget(*request.args['key'], encoding='utf-8')
        values = map(json.loads, values)
        return response.json(dict(zip(request.args['key'], values)))
    else:
        value = await app.redis_connection.get(request.args['key'], encoding='utf-8')
        value = json.loads(value)
        return response.json({request.args['key']: value})


@app.route('/set', methods=['POST'])
async def set_handler(request):
    """Set value(s) for key(s).

    Use SET for single key, MSET for multiple.
    """
    if len(request.json) > 1:
        await app.redis_connection.mset(*(
            x for key, value in request.json.items() for x in (key, json.dumps(value))
        ))
    else:
        key, value = list(request.json.items())[0]
        await app.redis_connection.set(key, json.dumps(value))
    return response.json(request.json)


app.register_listener(startup_connection, 'after_server_start')
app.register_listener(shutdown_connection, 'before_server_stop')
