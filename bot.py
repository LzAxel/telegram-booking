from config import BOT_TOKEN, DATABASE_URL
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
from database import Database
import logging

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
db = Database(DATABASE_URL)

