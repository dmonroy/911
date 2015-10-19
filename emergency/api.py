from chilero import web


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


routes = [
    ['/', Index],
    ['/squad/', Squad],
]
