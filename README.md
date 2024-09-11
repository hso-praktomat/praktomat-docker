# Running Praktomat in a Docker container

## TL;DR

```bash
docker network create praktomat
cd praktomat
docker build -t praktomat .
cd ..

# Edit template.env so that PRAKTOMAT_CHECKER_EXTERNAL_DIR points to an existing directory
docker-compose --env-file=template.env up -d

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

First, you need to build the Praktomat image. By doing this manually, Docker won't build an extra image for each instance. Naviagate into `praktomat` and build the image with the following command.

```bash
docker build -t praktomat .
```

Navigate back to the root directory of this repository. The following environment variables need to be set for running the container.

- `COMPOSE_PROJECT_NAME`: This is the ID of your Praktomat instance. Practically, this defines where you'll reach your Praktomat instance, e.g. https://localhost/your-praktomat-id.
- `PRAKTOMAT_NAME`: This is the name of your site. It will be displayed at the top of the web interface.
- `PRAKTOMAT_ADMIN`: The email address of the administrator for the Praktomat instance
- `PRAKTOMAT_DOMAIN`: The domain under which your instance(s) will be reachable
- `PRAKTOMAT_EXTERNAL`: The path to a directory that will be accessible via a bind mount in the Praktomat instance at `/external`
- `PRAKTOMAT_PRODUCTIVE`: The variable will enable the TLS protocol in the `docker-compose.yml`. For local tests on localhost the variable should be set to `false`.

Those variables are defined through an environment file. There's a template called `template.env`. Make a copy for each Praktomat instance and modify the contained variables to your needs.

Create a directory called `praktomat/work-data` in your home directory. Then create a subdirectory with the name of `COMPOSE_PROJECT_NAME` for each instance. The submissions for an instance will be stored here.

Create a directory called `praktomat/postgresql` in your home directory. Then create a subdirectory with the name of `COMPOSE_PROJECT_NAME` for each instance. The database for an instance will be stored here.

Then start an instance by supplying your environment file. Create an ennvironment file, e.g. `aud-win-env`, for your lecture by copying
and adjusting `template.env`. The command looks like the following.

```bash
docker-compose --env-file=aud-win.env up -d
```

Two containers are going to be created and started. One container contains a PostgreSQL database and one container contains the actual Praktomat application.

Now, open the CLI of the Praktomat container you just started. The container name usually looks like `<COMPOSE_PROJECT_NAME>_praktomat`.

```bash
docker exec -it <container name> /bin/bash
```

Then execute the following command to interactively create a superuser:

```bash
python3 Praktomat/src/manage-local.py createsuperuser
```

The application is accessible on https://PRAKTOMAT_DOMAIN/COMPOSE_PROJECT_NAME.

## Overview page

An overview page for all running instances is available on
https://PRAKTOMAT_DOMAIN/.

To generate the overview page for all the instances running,
run `traefik/overview-page/generate.py` on the host system and supply all the
paths to the env files that shall be included. The Python package libPyshell
needs to be installed for the script to work.

## Operations

Here are some notes on operating praktomat.

- Directory `$HOME/praktomat/work-data/$COMPOSE_PROJECT_NAME/sent-mails` stores a
  logfile for each error that occurs while praktomat is
  running. (Normally, an email is sent in such a situation.)
- Firefox requires a full certificate chain in some situations. Make sure to
  point Traefik to a full certificate chain in this case. If you don't have
  this, you can generate it by appending the other certificates to your actual
  certificate (in case you're using .pem files). Don't prepend them though,
  otherwise you'll get an issue that the private key doesn't match.
  If you don't have the missing certificates, try using a browser that doesn't
  has issues similar to the ones from Firefox and extract them from there.
  Safari did the job for me.

## Developer setup

* Install docker.
* Create directories `$HOME/praktomat/work-data/generic` and `$HOME/praktomat/postgresql/generic`.
* Edit `template.env` so that `PRAKTOMAT_CHECKER_EXTERNAL_DIR` points to an existing directory.
* Uncomment the line `ports: ["8000:443"]` in `docker-compose.yaml`.
* Execute the following commands:

```
docker network create praktomat
cd praktomat
docker build -t praktomat .
cd ..

docker-compose --env-file=template.env up -d
```

* Now your praktomat instance is accessible at `http://localhost:8000/generic`
* Create the admin account with

```
docker exec -it generic /bin/bash
python3 Praktomat/src/manage-local.py createsuperuser
```

* You should now be able to perform a successful login.

### Testing a patch with this setup

* Develop your patch in the Praktomat repository.
* Save your patch with something like:

```
git diff > my_feature.patch
```

* Move the patch into `$HOME/praktomat/work-data/generic`.
* Open a console within the Praktomat container (for example with
  `docker exec -it generic /bin/bash`).
* Navigate to the Praktomat directory and apply the patch:

```
cd Praktomat
git apply ../work-data/my_feature.patch
```

* Leave the console and restart the Praktomat container with:

```
docker compose --env-file=template.env restart praktomat
```

* Your patch should now be applied. Test to see if everything is working as
  intended.
* Don't forget to clean up your container first the next time you want to apply
  a patch.
