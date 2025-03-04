# Book Library Project - Development

## Docker Compose

- Start the local stack with Docker Compose:

```bash
docker compose watch
```

- Now you can open your browser and interact with the backend URLs:

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:$PORT/docs

To check the logs, run (in another terminal):

```bash
docker compose logs
```

## Local Development

The Docker Compose files are configured so that each of the services is available in a different port in `localhost`.

## Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker compose`.

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

They also use some additional configurations taken from environment variables set in the scripts before calling the `docker compose` command.

After changing variables, make sure you restart the stack:

```bash
docker compose watch
```

## The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.
