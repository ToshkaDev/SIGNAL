# SIGNALDB
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-%20djangorestframework-blue)](https://pypi.org/project/djangorestframework/)
[![Dockerized](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/github/license/ToshkaDev/SIGNAL.svg)](LICENSE)
[![Requirements Status](https://img.shields.io/librariesio/release/pypi/django)](https://pypi.org/project/Django/)


A Django-based web application with a REST API and database backend for serving and querying the results produced using the [SIGNAL pipeline](https://github.com/ToshkaDev/signal-transduction).

> **This project is under active development. Expect frequent changes.**

## Overview
The application is built with Django 5.2.x and Django REST Framework, running inside a Docker environment with PostgreSQL as the database. The app includes:

**Data Loader**: Efficient management scripts for bulk-loading structured data into the database.

**REST API**: Fully featured RESTful endpoints built on modular Django and DRF views, providing structured and secure access to your data.

**Search & Filtering**: Powerful search capabilities and filters for API queries.

**Linked Models & Views**: A clean, relational data model connected to class-based views and serializers for logical, maintainable code architecture.

**Automatic Migrations**: Schema migrations are handled using Django’s migration framework, ensuring database evolution is reliable and version-controlled.

**Dockerized Environment**: Seamless local and production environments using Docker Compose, including PostgreSQL and other dependencies.

## Core Dependencies
- Django >=5.2, <5.3  
- djangorestframework  
- psycopg2-binary (PostgreSQL client)  
- ...others listed in [requirements.dev.txt](./requirements.dev.txt)

## Getting Started
- Build the Docker containers: `make build-dev`
- Start the Django app and PostgreSQL database in development mode: `make up-dev`. The Django development server will be exposed at http://localhost:8000
- Load sample data: `make load_data` (takes ~5-7 min). Go to http://localhost:8000 to explore the API
- To execute the tests, use: `make test`
- To stop the development server, run: `make down-dev`

##  License
This project is licensed under the MIT License — see the [LICENSE](https://github.com/ToshkaDev/SIGNAL/blob/main/LICENSE) file for details.

