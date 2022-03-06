# Running Praktomat in a Docker container

## TL;DR

```bash
docker network create praktomat

SITE_NAME="Algorithmen und Datenstrukturen (WIN\/WINplus)" SERVER_ADMIN="hannes.braun@hs-offenburg.de" DOMAIN="progcheck.emi.hs-offenburg.de" COMPOSE_PROJECT_NAME=algdat-win docker compose up -d

cd traefik
docker compose up -d
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
docker compose up -d
```

Aside from the labels of other Docker containers, Traefik is configured through a static configuration file `traefik.toml` as well as a dynamic configuration file `traefik_dynamic.toml`. See the [Traefik docs](https://doc.traefik.io/traefik/) for more information.

## Starting a Praktomat instance

Navigate back to the root directory of this repository. If you're starting a particular instance for the first time, four environment variables need to be set for building the image.

- `COMPOSE_PROJECT_NAME`: This is the ID of your Praktomat instance. Practically, this defines where you'll reach your Praktomat instance, e.g. https://localhost/your-praktomat-id.
- `SITE_NAME`: This is the name of your site. It will be displayed at the top of the web interface.
- `SERVER_ADMIN`: The email address of the administrator for the Praktomat instance
- `DOMAIN`: The domain under which your instance(s) will be reachable

Since especially `SERVER_ADMIN` and `DOMAIN` won't change in most cases for different instances, there's an `.env` file setting default values for all of the environment variables. Modify it to your needs.

Then start an instance with the following command. "Real" environment variables will override those specified in the `.env` file.

```bash
SITE_NAME="Algorithmen und Datenstrukturen (WIN\/WINplus)" COMPOSE_PROJECT_NAME=algdat-win docker compose up -d
```

Two containers are going to be created and started. One container contains a PostgreSQL database and one container contains the actual Praktomat application. The submissions will be stored on a separate volume.

Now, open the CLI of the Praktomat container you just started. The container name usually looks like `<COMPOSE_PROJECT_NAME>-praktomat-1`.

```bash
docker exec -it <container name> /bin/bash
```

Then execute the following command to interactively create a superuser:

```bash
python3 Praktomat/src/manage-local.py createsuperuser
```

The application is accessible on https://DOMAIN/COMPOSE_PROJECT_NAME.

If you want to stop or remove the instance, it is now sufficient to only supply the project name (Praktomat ID).

```bash
COMPOSE_PROJECT_NAME=algdat-win docker compose stop
```
