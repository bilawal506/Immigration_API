from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

API_KEY = config("CHAT_GPT_API_KEY", cast=Secret)