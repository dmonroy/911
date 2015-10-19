import asyncio

import aiopg
from chilero import web
from emergency import ui, api
from emergency.db import parse_pgurl
from emergency.settings import get_settings

settings = get_settings()


def get_routes():
    return [
        ['/api{}'.format(item[0]), item[1]] for item in api.routes
    ] + [
        ['/ui{}'.format(item[0]), item[1]] for item in ui.routes
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
