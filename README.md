# REST interface for Redis

## deployment

Assume a Redis database running on localhost port 6379.

### local

```bash
pip install -r requirements.txt
export REDIS_HOST=localhost
export REDIS_PORT=6379
./main.py --port 6380
```

### Docker

```bash
docker build -t redis_rest .
docker run \
    -p 6380:6380 \
    --env REDIS_HOST=host.docker.internal \
    --env REDIS_PORT=6379 \
    redis_rest --port 6380
```

### docker-compose

To run both Redis database and REST interface, a docker-compose file is provided:

```bash
docker-compose up
```

## usage

http://localhost:6380/apidocs