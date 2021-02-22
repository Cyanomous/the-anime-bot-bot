from aiohttp import web

async def index(request):
    data = {"the best bot": "yes"}
    return web.json_response(data)


app = web.Application()
app.router.add_get("/", index)
web.run_app(app)