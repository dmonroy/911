from chilero import web


class Index(web.Resource):

    def index(self):
        return web.JSONResponse(
            dict(objects=[], meta=dict())
        )
