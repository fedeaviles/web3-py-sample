# Pull base image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --dev

COPY . /code/

EXPOSE 8000