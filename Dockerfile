#Dockerfile for building the project
#pull python as base image
FROM python:3.12-slim

#change timezone
ENV TZ="America/New_York"
RUN date

#variables to use
#poetry version
ARG POETRY_VERSION=1.8.0

#setup python and poetry env
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# poetry's configuration:
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=$POETRY_VERSION

#update system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    nano \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /streamlit_mpa_template
ADD streamlit_mpa_template  .
#copy poetry
COPY pyproject.toml .
COPY poetry.lock .
#install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install --only=main --no-interaction --no-ansi --no-root

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://0.0.0.0:8000/_stcore/health
#dev mode
#ENTRYPOINT ["tail", "-f", "/dev/null"]
#prod
ENTRYPOINT ["streamlit", "run", "streamlit_mpa_template.py", "--server.port=8000", "--server.address=0.0.0.0"]
