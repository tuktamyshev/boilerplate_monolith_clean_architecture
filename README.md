# FastAPI Clean Architecture Boilerplate

A template project for FastAPI applications following clean architecture principles.

### Getting Started

###### JWT Setup

For local development, you can generate JWT keys using our script:

```bash
# Make the script executable
chmod +x ./generate_jwt_keys.sh

# Generate JWT keys
./generate_jwt_keys.sh
```

This will create:
- `certs/jwt_private.pem` - Private key for signing tokens
- `certs/jwt_public.pem` - Public key for verifying tokens
1. Override environment variables in `.env` for local development if needed (defaults to `.env.default`)
2. Override environment variables in `.env.docker` for Docker deployment if needed (defaults to `.env.default`)

```shell
# For local development, install dependencies using uv
uv sync
```

Most likely, you will want to run all services in containers, and the application itself in the IDE,
then you should not forget to register host=localhost and port=9092 for kafka in env.docker,
then kafka will start in docker and you can connect to it from localhost.
You can copy .en.example to .env and .env.docker.example to .env.docker and everything will work.

### Make Commands

* `make all` - Run all services in containers
* `make all-down` - Stop all application containers (app, database, kafka)
* `make app-logs` - View application logs in container
* `make app-shell` - Access application shell in container

all same for db, kafka, redis
