import asyncio
from aiohttp import web

# CORS middleware
# https://gist.github.com/espretto/919a64d6a48e06da0fcf26ea70a50a93
ALLOWED_HEADERS = ','.join((
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-requested-with',
    'x-csrftoken',
    ))

def set_cors_headers (request, response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Methods'] = request.method
    response.headers['Access-Control-Allow-Headers'] = ALLOWED_HEADERS
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@asyncio.coroutine
def cors_factory (app, handler):

    @asyncio.coroutine
    def cors_handler (request):
        # preflight requests
        if request.method == 'OPTIONS':
            return set_cors_headers(request, web.Response())
        else:
            response = yield from handler(request)
            return set_cors_headers(request, response)

    return cors_handler
