#!/bin/sh -e

case "$1" in
  "server") gunicorn -b 0.0.0.0:5000 --workers 2 --threads 8 rebalance_server:app;;
  *) exec "$@" ;;
esac