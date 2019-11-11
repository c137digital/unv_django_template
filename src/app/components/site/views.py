from aiohttp import web

from unv.web.helpers import url_for_static
from unv.web.deploy import SETTINGS as DEPLOY_SETTINGS

from .settings import SETTINGS


async def index(request):
    st = url_for_static('example/2.txt')
    rd = request.app['redis']
    test = f'135 {st} {DEPLOY_SETTINGS.instance} {SETTINGS._data}\n'
    return web.Response(body=test)
