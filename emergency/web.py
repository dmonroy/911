import aiopg
import asyncio
from chilero import web
from emergency import api
from emergency.db import parse_pgurl
from emergency.settings import get_settings

settings = get_settings()


class HomeView(web.View):

    def get(self):
        return web.Response('This is the home!')


def api_routes():
    return [
        ['/', api.Index],
        ['/squad/', api.Squad],
    ]


def ui_routes():
    return [
        ['/', HomeView]
    ]


def get_routes():
    return [
        ['/api{}'.format(item[0]), item[1]] for item in api_routes()
    ] + [
        ['/ui{}'.format(item[0]), item[1]] for item in ui_routes()
    ]


class Application(web.Application):

    @asyncio.coroutine
    def get_pool(self):  # pragma: no cover
        if not hasattr(self, '_pool'):

            self._pool = yield from aiopg.create_pool(
                **parse_pgurl(settings.db_url)
            )

        return self._pool


def run_web():  # pragma: no cover
    web.run(Application, get_routes())


if __name__ == '__main__':  # pragma: no cover
    run_web()


if __name__ == 'emergency.web':  # pragma: no cover
    app = Application(routes=get_routes())
