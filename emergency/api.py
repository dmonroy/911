import json

from chilero import web
from psycopg2._json import Json


class Index(web.Resource):

    def index(self):
        return web.JSONResponse(
            dict(
                squads='/api/squad/'
            )
        )


class DBResource(web.Resource):

    list_query = None
    object_query = None

    def index(self):
        pool = yield from self.app.get_pool()
        objects = []

        with (yield from pool.cursor()) as cur:
            yield from cur.execute(self.list_query)
            for row in (yield from cur.fetchall()):
                objects.append(self.serialize_list_object(row))

        return web.JSONResponse(
            dict(
                objects=objects
            )
        )

    def serialize_list_object(self, row):  # pragma: no cover
        return row


class Squad(DBResource):

    list_query = 'select * from squad'
    object_query = list_query

    def serialize_list_object(self, row):
        return dict(
            id=row[0],
            name=row[1],
            url='/api/squad/{}/'.format(row[0])
        )

    def new(self):
        yield from self.request.post()
        name = self.request.POST['name']

        pool = yield from self.app.get_pool()

        with (yield from pool.cursor()) as cur:
            yield from cur.execute(
                'insert into squad (name) values (%s)', (name,)
            )

        return web.JSONResponse(
            dict(
                success=True
            )
        )


class Zone(DBResource):

    list_query = 'select * from zone'
    object_query = list_query

    def serialize_list_object(self, row):
        return dict(
            id=row[0],
            name=row[1],
            meta=row[2],
            url='/api/zone/{}/'.format(row[0])
        )

    def new(self):
        yield from self.request.post()
        name = self.request.POST['name']
        meta = json.loads(self.request.POST['meta']) \
            if self.request.POST.get('meta', None) else None

        meta = meta or {}

        pool = yield from self.app.get_pool()

        with (yield from pool.cursor()) as cur:
            yield from cur.execute(
                'insert into zone (name, meta) values (%s, %s)',
                (name, Json(meta))
            )

        return web.JSONResponse(
            dict(
                success=True
            )
        )


routes = [
    ['/', Index],
    ['/squad/', Squad],
    ['/zone/', Zone],
]
