from aiohttp import request
from chilero.web.test import WebTestCase, asynctest
from emergency.web import get_routes


class TestBase(WebTestCase):
    routes = get_routes()

    @asynctest
    def test_view(self):
        resp = yield from request(
            'GET', self.full_url('/'), loop=self.loop
        )

        self.assertEqual(resp.status, 200)

        text = yield from resp.text()

        self.assertEqual('This is the home!', text)

    def test_import_gunicorn(self):
        # Check that emergency/gunicorn_config.py doesn't raise any exception

        from emergency.gunicorn_config import proc_name

        assert proc_name == 'emergency'

