#!/bin/bash

set -e

# Run any necessary startup commands here, like migrations
# echo "Running startup commands..."

# Start Uvicorn with app module, host, and port from environment variables
exec uvicorn app.main:fastapi_app --host 0.0.0.0 --port 5001 --reload

DB_CHECK_INTERVAL=${DB_CHECK_INTERVAL:-5}
DB_CHECK_RETRIES=${DB_CHECK_RETRIES:-120}

pg_isready() {
  i=0
  echo -n "waiting for database connection "
  while [ ${i} -le ${DB_CHECK_RETRIES} ]; do
    python pg_isready.py && return || echo -n "."
    sleep ${DB_CHECK_INTERVAL}
    let i++
  done
}

ACTION=""
if [ $# -ge 1 ]; then
  ACTION=${1} ; shift
fi

case "${ACTION}" in

  ''|-*)
    pg_isready
    exec uvicorn ${UVICORN_APP} ${ACTION} ${@}
    ;;

    uvicorn)
    pg_isready
    exec uvicorn ${UVICORN_APP} ${@}
    ;;

    migration)
      pg_isready
      exec alembic -c app/migrations/alembic.ini upgrade head
      ;;

    pytest)
    pg_isready
    exec pytest ${@}
    ;;

    noexit)
      # used locally for docker-based development
      # so things don't shut down after the process ends/exits.
      while sleep 1000; do :; done
      ;;

    *)
      exec ${ACTION} ${@}
      ;;

esac
