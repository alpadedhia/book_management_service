#
# Dependencies stage
#   This stage focuses on:
#     1. Adding OS dependencies required to build / compile packages
#     2. Update poetry's lock file to ensure last changes to pyproject.toml are present
#     3. Install dependencies for the application
#     4. Generate requirements-dev.txt out of poetry
#
#   Poetry is not used to install packages as it uses a virtualenv
#   which needs to be avoided in containers
#
FROM python:3.12-slim-bullseye AS deps

ENV POETRY_VERSION  1.5.1


#
# OS dependencies required by python packages should go here,
# dev packages and libraries
#
RUN apt-get update && apt-get install --no-install-recommends -y \
  gcc \
  libc-dev \
  libpq-dev \
  libpq5 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
COPY ./pyproject.toml /tmp

#
# This section focuses on:
#   1. Generate requirements.txt and requirements-dev.txt using poetry
#   2. Install packages from requirements.txt
#
#   The packages installed in /usr/local/lib/python<version>/site-packages will
#   be copied onto the base stage
#

RUN pip install -q --no-cache-dir poetry==$POETRY_VERSION \
  && poetry lock -q -n \
  && poetry export -f requirements.txt -o /tmp/requirements.txt --without-hashes \
  && poetry export -f requirements.txt -o /tmp/requirements-dev.txt --without-hashes --without-urls --only dev \
  && pip uninstall -y poetry \
  && pip install --no-cache-dir -q -r /tmp/requirements.txt

#
# Base stage
#   Contains all defaults that will be used as the base stage for
#   production and development images
#

FROM python:3.12-slim-bullseye AS base

ENV APP_NAME    book_management
ENV PREFIX      /opt/jk_tech
ENV PREFIX_APP  ${PREFIX}/${APP_NAME}

ENV UVICORN_HOST    0.0.0.0
ENV UVICORN_PORT    5001
ENV UVICORN_APP     app.main:fastapi_app

ENV PYTHONUNBUFFERED 1

RUN groupadd -g 20001 jk_tech \
  && useradd -l -M -u 10001 -g jk_tech jk_tech

WORKDIR ${PREFIX_APP}

COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]

RUN apt-get update && apt-get install --no-install-recommends -y libpq5 \
  && rm -rf /var/lib/apt/lists/*

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin
COPY . ${PREFIX_APP}

RUN chown -R jk_tech:jk_tech ${PREFIX_APP}

#
# Development stage
#

FROM base AS dev

ENV PYTHONDONTWRITEBYTECODE 1

#
# OS dependencies that need to be present for development and debugging purposes to work
# must be installed here.
# ONLY DEV LIBRARIES
#
RUN apt-get update && apt-get install --no-install-recommends -y git curl dnsutils \
  && rm -rf /var/lib/apt/lists/*

COPY --from=deps /tmp/requirements-dev.txt /tmp/requirements-dev.txt

RUN pip install --no-cache-dir -q -r /tmp/requirements-dev.txt

#
# Upstream image
#

FROM base

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

USER jk_tech

EXPOSE 3000
