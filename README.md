# condor

This is the condor service. It is built on [Baseplate].

[Baseplate]: https://reddit.github.io/baseplate/


## Database Initialization

To create schema in the database:

    baseplate-script2 example.ini condor.models:create_schema

## Development

### Vagrant

A `Vagrantfile` and associated puppet manifests describing a development
environment are provided. Launch a development VM with:

    vagrant up

Once provisioning is complete, then start the server as usual:

    vagrant ssh
    cd condor/
    baseplate-serve2 --bind 0.0.0.0:9090 --reload --debug example.ini

Run `vagrant provision` whenever you change the puppet manifests for new
dependencies etc.

### Docker


A `Dockerfile` for the service and `docker-compose.yml` that launches a
development environment are provided. Start the development server with:

    docker-compose build
    docker-compose up

Changes to the code will automatically restart the server. Re-run the build
command any time you change dependencies.

### Testing

The test suite lives under `tests/`. Exercise it by running:

    nosetests
