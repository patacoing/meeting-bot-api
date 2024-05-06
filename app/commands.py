import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import requests
from json import loads
from app.settings import settings

# global commands are cached and only update every hour
# url = f'https://discord.com/api/v10/applications/{APP_ID}/commands'

# while server commands update instantly
# they're much better for testing

url = f'https://discord.com/api/v10/applications/{settings.APP_ID}/guilds/{settings.SERVER_ID}/commands'

json = loads(open(settings.COMMANDS_FILENAME).read())

response = requests.put(url, headers={
    'Authorization': f'Bot {settings.BOT_TOKEN}'
}, json=json)

print(response.status_code)
