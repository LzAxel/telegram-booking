from dotenv import load_dotenv
from os import environ
from pathlib import Path

load_dotenv(Path('cfg/.env'))

BOT_TOKEN = environ.get('BOT_TOKEN')
DATABASE_URL = environ.get('DATABASE_URL')