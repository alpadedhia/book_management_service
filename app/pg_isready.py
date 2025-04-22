#!/usr/bin/env python
# vim: ts=2:sw=2:et:

from os import environ as env
from urllib.parse import quote_plus

import psycopg2

config = {
    "host": env.get("DATABASE_HOSTNAME"),
    "port": env.get("DATABASE_PORT"),
    "user": env.get("DATABASE_USER"),
    "pass": quote_plus(env.get("DATABASE_PASSWORD")),
    "database": env.get("DATABASE_DB"),
}

dsn = "postgresql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s" % config

if __name__ == "__main__":
    try:
        db = psycopg2.connect(dsn)
    except (Exception, psycopg2.DatabaseError):
        exit(1)

    exit(0)
