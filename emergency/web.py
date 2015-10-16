from chilero import web


class HomeView(web.View):

    def get(self):
        return web.Response('This is the home!')


def get_routes():
    return [
        ['/', HomeView],
    ]


def run_web():  # pragma: no cover
    web.run(web.Application, get_routes())


if __name__ == '__main__':  # pragma: no cover
    run_web()


if __name__ == 'emergency.web':  # pragma: no cover
    app = web.Application(routes=get_routes())
