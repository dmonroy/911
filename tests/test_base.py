from aiohttp import request
import asyncio
from chilero.web.test import WebTestCase, asynctest
import pytest
from emergency.db import get_pool
from emergency.settings import get_settings
from emergency.web import get_routes, Application

settings = get_settings()


@pytest.fixture
def conn():

    pool = yield from get_pool()
    conn = yield from pool.acquire()
    yield conn

    yield from pool.release(conn)


class TestBase(WebTestCase):
    routes = get_routes()
    application = Application

    @asynctest
    def test_ui_home_view(self):
        resp = yield from request(
            'GET', self.full_url('/ui/'), loop=self.loop
        )

        self.assertEqual(resp.status, 200)

        text = yield from resp.text()

        self.assertEqual('This is the home!', text)
        resp.close()

    @asynctest
    def test_api_home_view(self):
        resp = yield from request(
            'GET', self.full_url('/api/'), loop=self.loop
        )

        self.assertEqual(resp.status, 200)
        resp.close()

    def test_import_gunicorn(self):
        # Check that emergency/gunicorn_config.py doesn't raise any exception

        from emergency.gunicorn_config import proc_name

        assert proc_name == 'emergency'

    def test_import_cli(self):
        # Check that emergency/cli.py doesn't raise any exception

        from emergency.cli import main


class TestDatabase(WebTestCase):
    routes = get_routes()
    application = Application

    @asynctest
    def test_database(self):
        pool = yield from self.app.get_pool()

        with (yield from pool.cursor()) as cur:
            yield from cur.execute('select now()')
            r = yield from cur.fetchone()
            assert len(r) == 1

    @asynctest
    def test_squad_table(self):
        pool = yield from self.app.get_pool()

        with (yield from pool.cursor()) as cur:
            yield from cur.execute('select count(1) from squad')
            r = yield from cur.fetchone()
            assert len(r) == 1
            assert r[0] == 0

            for i in range(10):
                yield from cur.execute(
                    'insert into squad (name) values (%s)',
                    ('squad {}'.format(i),)
                )

            yield from cur.execute('select count(1) from squad')
            r = yield from cur.fetchone()
            assert len(r) == 1
            assert r[0] == 10


class TestApiIndex(WebTestCase):
    routes = get_routes()
    application = Application

    @asynctest
    def test_index(self):
        resp = yield from request(
            'GET', self.full_url('/api/'), loop=self.loop,
        )

        self.assertEqual(resp.status, 200)


class TestSquadResource(WebTestCase):
    routes = get_routes()
    application = Application

    @asynctest
    def test_index(self):
        resp = yield from request(
            'GET', self.full_url('/api/squad/'), loop=self.loop,
        )

        self.assertEqual(resp.status, 200)
        resp.close()

    @asynctest
    def test_create(self):
        data = dict(
            name='New Squad'
        )
        resp = yield from request(
            'POST', self.full_url('/api/squad/'), loop=self.loop,
            data=data
        )

        self.assertEqual(resp.status, 200)
        resp.close()

        resp = yield from request(
            'GET', self.full_url('/api/squad/'), loop=self.loop,
        )

        self.assertEqual(resp.status, 200)
        resp.close()

