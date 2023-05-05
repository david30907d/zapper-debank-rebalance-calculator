# Use the official Python base image with Alpine
FROM python:3.11.3-alpine3.17

# Set the working directory
WORKDIR /rebalance_server

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV POETRY_VERSION 1.4.2
ENV POETRY_HOME "/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV PATH "$POETRY_HOME/bin:$PATH"
# Install system dependencies
RUN apk update \
  && apk add --no-cache \
    build-base \
    curl \
    libffi-dev \
    openssl-dev \
    postgresql-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Copy the `pyproject.toml` and `poetry.lock` files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry export --without-hashes -f requirements.txt -o ./requirements.txt \
    && pip install --user --no-cache-dir --no-warn-script-location -r ./requirements.txt \
    # Cleaning poetry installation's cache for production:
    && rm -rf "$POETRY_CACHE_DIR" \
    && apk del curl \
    && pip uninstall -yq poetry \
    && rm -rf /tmp/* /var/cache/apk/*
# RUN poetry config virtualenvs.create false \
#   && poetry install --no-interaction --no-ansi

# Copy the app files
COPY . .
WORKDIR /
COPY docker-entrypoint.sh docker-entrypoint.sh

# Expose the default Flask port
EXPOSE 5000

# Setup ENTRYPOINT
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["server"]