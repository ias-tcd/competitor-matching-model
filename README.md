# Competitor matching model

This repo contains the source code for the machine learning models used for TCD SwEng Group 20's project with Integral
Ad Science - a competitor matching machine learning model.

The project is built using python and runs inside Docker containers.

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
\venv/Scripts\activate.bat

# Install the local and project dependencies
pip install -r requirements.local.txt

# Install the pre-commit hooks
pre-commit install

# Build the docker container
make build

# Run the application
make run
```

## Useful Commands

Below are some useful commands and what they do

```bash
# Remove the docker container (helpful if there is an issue with your build such as caching old dependencies)
make down

# Remove the docker container and restart the application (building a new container)
make restart

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
