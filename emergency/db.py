import os
from urllib.parse import urlsplit

import aiopg
import asyncio
from schema_migrations import MigrationController
from emergency.settings import get_settings

settings = get_settings()


@asyncio.coroutine
def get_pool():  # pragma: no cover
    '''
    Gets the postgresql connection pool.

    Checks the existence of a connection pool, if it doesn't exists then
    attempts to create a pool. Only a pool is active per instance.

    :return: pool
    '''

    if 'pool' not in globals():
        global pool
        pool = yield from aiopg.create_pool(
            **parse_pgurl(settings.db_url)
        )

    return pool


def parse_pgurl(url):
    '''
    Given a Postgres url, return a dict with keys for user, password,
    host, port, and database.
    '''
    parsed = urlsplit(url)

    return {
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/'),
        'host': parsed.hostname,
        'port': parsed.port,
    }


def create_database():  # pragma: no cover
    '''
    Creates the postgresql database and runs all migrations.
    '''
    import psycopg2  # isort:skip
    settings = get_settings()
    dbdata = parse_pgurl(
        'psycopg2+postgresql://postgres@localhost:5432/postgres'
    )
    new_dbdata = parse_pgurl(settings.db_url)
    conn = psycopg2.connect(**dbdata)
    conn.set_isolation_level(0)
    cur = conn.cursor()

    cur.execute('CREATE DATABASE {}'.format(new_dbdata['database']))
    cur.close()
    conn.close()

    run_migrations()


def drop_database():  # pragma: no cover
    '''
   Deletes the existing postgresql database.
    '''
    import psycopg2  # isort:skip
    settings = get_settings()
    dbdata = parse_pgurl(
        'psycopg2+postgresql://postgres@localhost:5432/postgres'
    )
    new_dbdata = parse_pgurl(settings.db_url)
    conn = psycopg2.connect(**dbdata)
    conn.set_isolation_level(0)
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS {}'.format(new_dbdata['database']))
    cur.close()
    conn.close()


def run_migrations():  # pragma: no cover
    '''
    Executes all database migrations into the database.
    '''
    mc = MigrationController(
        databases=dict(
            emergency=settings.db_url,
        ),
        groups=dict(
            emergency=os.path.join(os.getcwd(), 'emergency/migrations')
        )
    )

    mc.migrate()
