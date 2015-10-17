from chilero import web
from emergency import api


class HomeView(web.View):

    def get(self):
        return web.Response('This is the home!')


def api_routes():
    return [
        ['/', api.Index],
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


def run_web():  # pragma: no cover
    web.run(web.Application, get_routes())


if __name__ == '__main__':  # pragma: no cover
    run_web()


if __name__ == 'emergency.web':  # pragma: no cover
    app = web.Application(routes=get_routes())
