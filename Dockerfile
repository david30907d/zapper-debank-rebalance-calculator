# Use the official Python base image with Alpine
FROM python:3.11.3-slim

# Set the working directory
WORKDIR /rebalance_server

# Set environment variables
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# Install Poetry
RUN pip install --no-cache-dir -U pip==23.1.2 \
    && pip install --no-cache-dir poetry==1.4.2

# Copy the `pyproject.toml` and `poetry.lock` files
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
# Install project dependencies
RUN poetry export --without-hashes -f requirements.txt -o ./requirements.txt \
    && pip install --no-cache-dir --no-warn-script-location -r ./requirements.txt \
    # Cleaning poetry installation's cache for production:
    && rm -rf "$POETRY_CACHE_DIR" \
    && pip uninstall -yq poetry \
    && rm -rf /tmp/* /var/cache/apk/*
# Copy the app files
COPY . .
WORKDIR /
# COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.sh docker-entrypoint.sh
# Expose the default Flask port
EXPOSE 5000

# Setup ENTRYPOINT
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["server"]
