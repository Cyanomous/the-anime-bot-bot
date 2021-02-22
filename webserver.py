mport web
import aiohttp_jinja2
import jinja2
from pathlib import Path
import json
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

async def index(request):
    data = {"the best bot": "yes"}
    return web.json_response(data)


app = web.Application()
app.router.add_get("/", index)
web.run_app(app)