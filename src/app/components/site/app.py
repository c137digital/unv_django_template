from aiohttp import web

from . import views


def setup(app: web.Application):
    app.router.add_get('/', views.index, name='index')
