FROM python:3.7

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION:-latest}

RUN mkdir -p /app

WORKDIR /app

RUN set -ex \
    # Install General Build Dependencies
    && apt-get update -qq -y --no-install-recommends \
    && apt-get upgrade -y --no-install-recommends \
    && cd /app

ADD . /app/

# set up dependencies
RUN sh dependencies.sh \
    # Delete build dependencies
    && rm -rf /tmp/* \
    && apt-get autoremove -y \
    && apt-get purge -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

CMD ["/app/launch.sh"]
