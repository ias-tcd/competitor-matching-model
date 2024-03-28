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

Due to the GitHub organisation being a free organisation, we are somewhat limited by the number of files we can track using git LFS.
So we had to revert to tracking images with regular git tracking and save LFS for the weights files.
This overwrote the git history, so to clean this up, we have provided a `.git-blame-ignore-revs` file to be used if checking for commit authors.
So instead of `git blame <file-name>`, you can use `git blame <file-name> --ignore-revs-file=.git-blame-ignore-revs` to see the cleaner history.

## Running an individual model

You may want to run custom or specific code on a given model without the API for local testing.
What you need to do is create a `main.py` file in `ml/models/<model to test>` directory and add a `main` function to it.
In the `main` function you can add any needed code, see [this example](/ml/models/logo_detection/main.py) for testing with an image.
The code loads an image from the working directory (root directory of the repository) and runs inference using our logo detection model on it.

```python
import logging

from .process import process

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main():
    input_image_path = "my_image.jpeg"
    inferences = process(input_image_path)

    for inference in inferences:
        logger.info(f"x: {inference.bounding_box.x}")
        logger.info(f"y: {inference.bounding_box.y}")
        logger.info(f"Width: {inference.bounding_box.w}")
        logger.info(f"Height: {inference.bounding_box.h}")
        logger.info(f"Confidence score: {inference.confidence}\n")


if __name__ == "__main__":
    main()
```

To run the script, run `make model name=<model to test>` where `<model to test>` is the subdirectory of `ml/models` that the model you want to test is in.
So for the above example, you would run `make model name=logo_detection`.

If the image is not in the root directory of the repository, but is inside the repository somewhere, you can use an absolute path for accessing it.
Say the image is stored in `ml/models/my_image.png`, then you would change the path in `main.py` to `/src/ml/models/my_image.py` or `ml/models/my_image.png`.
Note the leading `/` in the first option and lack of it in the second option.

## Running the full flow from the command line

To run the full command line flow with no database persistence do the following:

1. Add the image you want to test to the root directory of the repository - take note of the name
2. Run `make detect-infer name=<image name>`. The image name must also include the file extension

The result should be something like this, printed to the console:

```
...
INFO:root:Done. (1.605s)
1/1 ━━━━━━━━━━━━━━━━━━━━ 1s 611ms/step
INFO:root:Brands detected in order: ['under_armour', 'under_armour', 'north_face', 'new_balance'] with bbox: LogoDetectionInference(bounding_box=BoundingBox(x=0.3321428596973419, y=0.14478416740894318, w=0.12857143580913544, h=0.09892086684703827), confidence=0.21258708834648132, overlap=False)
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 106ms/step
INFO:root:Brands detected in order: ['under_armour', 'new_balance', 'north_face', 'under_armour'] with bbox: LogoDetectionInference(bounding_box=BoundingBox(x=0.5866071581840515, y=0.308453232049942, w=0.12678571045398712, h=0.09892086684703827), confidence=0.2793073356151581, overlap=False)
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 104ms/step
INFO:root:Brands detected in order: ['under_armour', 'north_face', 'new_balance', 'under_armour'] with bbox: LogoDetectionInference(bounding_box=BoundingBox(x=0.8410714268684387, y=0.4739208519458771, w=0.12857143580913544, h=0.09892086684703827), confidence=0.29989734292030334, overlap=False)
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
