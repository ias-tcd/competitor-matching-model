# Competitor matching model

[![AWS Deployment](https://github.com/ias-tcd/competitor-matching-model/actions/workflows/deploy.yml/badge.svg)](https://github.com/ias-tcd/competitor-matching-model/actions/workflows/deploy.yml)
[![Tests](https://github.com/ias-tcd/competitor-matching-model/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/ias-tcd/competitor-matching-model/actions/workflows/build-and-test.yml)
[![Linting](https://github.com/ias-tcd/competitor-matching-model/actions/workflows/lint-and-format.yml/badge.svg)](https://github.com/ias-tcd/competitor-matching-model/actions/workflows/lint-and-format.yml)

This repo contains the source code for the machine learning models and the api used for TCD SwEng Group 20's project with Integral
Ad Science - a competitor matching machine learning model.

The project is built using python and runs inside Docker containers.
The api is built using Django and connects to a PostgreSQL database. This api is used to allow the front end application to communicate with the back end.

## Version Requirements

The following must be installed to run and develop this source code:

|   Dependency   |     Version     |                   Install                   |
| :------------: | :-------------: | :-----------------------------------------: |
|     Docker     |      24.\*      | [docs](https://docs.docker.com/get-docker/) |
| docker-compose |      2.\*       |       Will install with docker above        |
|     Python     | 3.11 or higher  |  [docs](https://www.python.org/downloads/)  |
|      Pip       | 23.\* or higher |      Should install with python above       |

## First steps

After cloning the repository do the following:

Note you may have to use `python3` or `pip3` in place of `python` and `pip` respectively.

```bash
# Create the virtual environment
# Note: if you choose not to name it 'venv', add the name to the .gitignore file before committing anything
# For mac / linux
python -m venv venv
source venv/bin/activate

# For windows
virtualenv venv
\venv\Scripts\activate.bat

# Install the local and project dependencies
pip install -r requirements.local.txt

# Install the pre-commit hooks
pre-commit install

# Add an environment file and start by populating it with the frontend url
echo FRONTEND_URL=http://localhost:5173 >> .env

# Build the docker container
make build

# Run Django migrations
# These represent database schema changes and need to be run every time the database structure changes
# (e.g. new tables adding, table structure changing)
make migrate

# Run the application
make run
```

To work with the larger files in this repository (such as the model weights), you should install [git lfs](git-lfs.com).
You can download it from the website or using homebrew or similar.
You must then install it locally:

```bash
# Install via homebrew (on macOS)
brew install git-lfs

# After installation
git lfs install
```

## Deployments

This API is deployed to AWS using Docker and GitHub Actions. The API can be accessed at the following [url](http://3.254.180.26).
In the `/docker` directory you will find `entrypoint.sh` and `docker-compose.prod.yml`. Alongside the deployment script in `.github/workflows/deploy.yml`, this builds a slim version of the API image and pushes the image to the GitHub Container Registry. These images are pulled down in the AWS EC2 instance and used to spin up the containers.
There are three production containers: `api`, `db` and `nginx`. `api` is used to receive REST requests from our front end client and uses the `db` to persist information. Django (the framework this API is built in) also provides a powerful admin interface which must be served statically. We use `nginx` here to both serve the static files and pass requests to the API.

## Documentation

We have provided simple API documentation for any of the endpoints we have built here. These are of course useful for external people to look at our project and gain a better understanding of how it works but is also useful as a reference for our team members, particularly those on the front end team. You can view the documentation [here](/docs/README.md).

## Useful Commands

Below are some useful commands and what they do

```bash
# Remove the docker container (helpful if there is an issue with your build such as caching old dependencies)
make down

# Remove the docker container and restart the application (building a new container)
make restart

# Make migrations for schema changes
make migrations

# Migrate changes to the database for schema changes
make migrate

# Start the python interpreter to manually run specific code / functions
make shell

# Run the whole test API suite
make test

# Run individual API test(s)
# Here `path` should be the path of the test file(s) relative to the `/api/tests/` directory, and should be separated by `.` not `/`
make test path=<path.to.tests>

# Create a new django app
make startapp name=name_of_app

# Enter the container in the shell
make enter

# Format the code
make format

# Format the code for a specific directory
make format path=path/to/directory

# Lint the code
make lint

# Lint the code for a specific directory
make lint path=path/to/directory
```

## Pre-Commit Hooks

This project uses [pre-commit](https://pre-commit.com/) hooks to linting and formatting before allowing a commit to be
made. If the code being committed is not formatted well or has security issues, the terminal will show where the errors
are and these should be corrected before committing.
