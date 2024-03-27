import requests
import os
import sys
from dotenv import load_dotenv, find_dotenv
load_dotenv()

# add your env variables into a .env file in your root directory

headers = {"Authorization": "Key " + os.getenv("ptd_api_key")}


response = requests.get(
            os.getenv("ptd_server") + "__api__/v1/content/", headers=headers)

print(response.content)