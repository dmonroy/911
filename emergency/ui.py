from chilero import web


class HomeView(web.View):

    def get(self):
        return web.Response('This is the home!')


routes = [
    ['', HomeView]
]
