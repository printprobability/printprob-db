A Django-powered REST API for powering the data transformation and tagging pipeline for Print & Probability, a joint project between Carnegie Mellon University and University of California San Diego to identify typesets in early modern printed books.

The frontend is powered with VueJS, and styled via vue-bootstrap.

Images are served as IIIF, currently using [go-iiif-vips](https://github.com/cmu-lib/go-iiif-vips) as it can serve both JPEG as well as TIFF images on demand.

## Architecture

1. PostgreSQL database
2. Django REST API
3. Vue frontend
4. nginx reverse proxy

## Local development

### DB and API

`docker-compose.yml` defines a local development environment running Postgres as well as the Django API.

You must have a `.env` file in the same directory to supply configuration variables. Run `cp .template.env .env` and edit the file.

The `Makefile` defines almost all tasks needed for setting up and tearing down the development environment.

`make` will start up the service, which includes building the docker images if needed, creating a blank database `pp` in Postgres if it does not yet exist, and then starting the Django application to listen on `http://localhost:80/api/`. Most other make tasks require the service to be running in order to work. `make down` will shut down the containers and remove the Docker network (but data in the associated volumes will persist.)

When building the service for the first time in your local development environment, also run `make redeploy` once the system is running, in order to copy all the static files (html, css, and js) that Django uses to the correct Docker volume. This is only necessary on first startup - as long as you keep the docker volumes, the static files will stay in place in between invocations of `make` and `make down`

`make loadtest`/`make dumptest` loads and outputs test data defined in `app/pp/fixtures/test.json`. This test data has fake values for most fields, so note that the `tif` paths for images in the test data are not valid URLs and will display locally as broken.

To access the API, log in to the test account at `http://localhost/api/auth/login`:

username: `root`
password: `print&probability`

`make wipe` will drop the current database and recreate it, re-running migrations to create the necessary tables.

`make redeploy` will run all migrations against the current DB, and will refresh all static assets.

To run Django other management commands such as creating and running migrations, `make attach` will shell you into the Django container. `make db` will shell you into Postgres.

### Frontend

Currently using Node 16.14.0 and npm 8.3.1

```sh
cd vue
npm install
npm run serve
```

The local frontend will be available at `http://localhost:4000`. You must first log in to the test account at `http://localhost/api/auth/login` to test the frontend locally.

## Updating dependencies

We use [poetry](https://python-poetry.org/) to pin python package versions and calculate all dependencies for local development, however the docker container itself (and production deployment) only reads `requirements.txt`. Use poetry to update this file automatically:

```
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

## Contact

Maintained by [Matthew Lincoln](https://github.com/mdlincoln)
