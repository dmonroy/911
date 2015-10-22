from aiohttp import request
from chilero.web.test import asynctest
from tests.test_base import TestBase


class TestSquadResource(TestBase):

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
