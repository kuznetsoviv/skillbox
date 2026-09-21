from telebot import TeleBot
import os
from telebot.storage import StateMemoryStorage
from config_data import config

if config.PROXY_HOST:
    proxy_url = f"{config.PROXY_TYPE}://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_HOST}:{config.PROXY_PORT}"
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
