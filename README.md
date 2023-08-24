## Andersen API test project with Dockerized FastAPI and PostgreSQL

### How to lauch this project:

you would need Docker Desktop.

#### Clone this repo and move to project main directory:
    git clone https://github.com/Gudini108/Andersen-API-test-project.git

#### Launch your Docker Desktop application

#### Lauch project with `./scripts/run.sh` command

#### You would find Swagger documentation at `localhost:8080/docs/` or ReDoc documentation at `localhost:8080/redoc/`

#### To drop containers and clean Database use `./scripts/drop.sh` command

#### To launch unittests use `./scripts/test.sh` command


### Known issues:
For M1 and M2 Macbooks use `export DOCKER_DEFAULT_PLATFORM=linux/amd64` command beforehand
