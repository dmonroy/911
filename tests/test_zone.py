from aiohttp import request
from chilero.web.test import asynctest
from tests.test_base import TestBase


class TestZoneResource(TestBase):
    @asynctest
    def test_index(self):
        resp = yield from request(
            'GET', self.full_url('/api/zone/'), loop=self.loop,
        )

        self.assertEqual(resp.status, 200)
        resp.close()

    @asynctest
    def test_create(self):
        data = dict(
            name='New Zone',
            meta={}
        )
        resp = yield from request(
            'POST', self.full_url('/api/zone/'), loop=self.loop,
            data=data
        )

        self.assertEqual(resp.status, 200)
        resp.close()

        resp = yield from request(
            'GET', self.full_url('/api/zone/'), loop=self.loop,
        )

        self.assertEqual(resp.status, 200)
        resp.close()
