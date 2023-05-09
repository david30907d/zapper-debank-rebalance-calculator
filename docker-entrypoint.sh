#!/bin/sh -e

case "$1" in
  "server") flask --app rebalance_server --debug run -p 5000 --host=0.0.0.0 ;;
  *) exec "$@" ;;
esac