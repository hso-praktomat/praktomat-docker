# Running Praktomat in a Docker container

## TL;DR

```bash
docker network create praktomat

docker-compose --env-file=aud-win.env up -d

cd traefik
docker-compose up -d
```

## Initial setup

Create a network called `praktomat` to which the individual Praktomat instances as well as the reverse proxy will have access to.

```bash
docker network create praktomat
```

We're using [Traefik](https://github.com/traefik/traefik) as a reverse proxy for this setup. Traefik is responsible for the TLS encryption as well as the routing to the various Praktomat instances running on your host. 
Copy over the SSL/TLS certificate to `traefik/cert.pem` and the private key to `traefik/key.pem`. The routing to the individual Praktomat instances will happen automatically via labels.

Now, start up the Traefik container.
```bash
cd traefik
docker-compose up -d
```

Aside from the labels of other Docker containers, Traefik is configured through a static configuration file `traefik.toml` as well as a dynamic configuration file `traefik_dynamic.toml`. See the [Traefik docs](https://doc.traefik.io/traefik/) for more information.

## Starting a Praktomat instance

Navigate back to the root directory of this repository. The following environment variables need to be set for running the container.

- `COMPOSE_PROJECT_NAME`: This is the ID of your Praktomat instance. Practically, this defines where you'll reach your Praktomat instance, e.g. https://localhost/your-praktomat-id.
- `PRAKTOMAT_NAME`: This is the name of your site. It will be displayed at the top of the web interface.
- `PRAKTOMAT_ADMIN`: The email address of the administrator for the Praktomat instance
- `PRAKTOMAT_DOMAIN`: The domain under which your instance(s) will be reachable
- `PRAKTOMAT_EXTERNAL`: The path to a directory that will be accessible via a bind mount in the Praktomat instance at `/home/praktomat/external`

Those variables are defined through an environment file. There's a template called `template.env`. Make a copy for each Praktomat instance and modify the contained variables to your needs.

Create a directory called `work-data` in your home directory. Then create a subdirectory with the name of `COMPOSE_PROJECT_NAME` for each instance. The submissions for an instance will be stored here.

Then start an instance by supplying your environment file. The command looks like the following.

```bash
docker-compose up --env-file=aud-win.env -d
```

Two containers are going to be created and started. One container contains a PostgreSQL database and one container contains the actual Praktomat application.

Now, open the CLI of the Praktomat container you just started. The container name usually looks like `<COMPOSE_PROJECT_NAME>-praktomat`.

```bash
docker exec -it <container name> /bin/bash
```

Then execute the following command to interactively create a superuser:

```bash
python3 Praktomat/src/manage-local.py createsuperuser
```

The application is accessible on https://PRAKTOMAT_DOMAIN/COMPOSE_PROJECT_NAME.
