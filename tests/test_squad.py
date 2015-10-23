import json
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
        jresp = yield from resp.json()

        self.assertIn('objects', jresp)
        self.assertEqual(list, type(jresp['objects']))
        self.assertGreater(len(jresp['objects']), 0)

        for element in jresp['objects']:
            self.assertEquals({'id', 'name', 'url'}, set(element.keys()))

        resp.close()

    @asynctest
    def test_view(self):

        # Create some records in the database in case the table is empty
        for i in range(5):
            data = dict(
                name='Other Squad {}'.format(i)
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
        jresp = yield from resp.json()

        for element in jresp['objects']:
            url = element['url']
            eresp = yield from request(
                'GET', self.full_url(url), loop=self.loop,
            )
            self.assertEqual(eresp.status, 200)
            ejresp = yield from eresp.json()

            self.assertEquals({'id', 'name', 'url'}, set(ejresp.keys()))

            for k, v in element.items():
                self.assertEqual(v, ejresp[k])

            eresp.close()

        resp.close()

    @asynctest
    def test_view_404(self):

        resp = yield from request(
            'GET', self.full_url('/api/squad/999999'), loop=self.loop,
        )

        self.assertEqual(resp.status, 404)

        resp.close()
