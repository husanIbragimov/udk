import os

from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = os.getenv('ADMINS').split(', ')
CHANNELS = os.getenv('CHANNEL_ID', '-1001275637856').split(', ')
TELEGRAM_API = os.getenv('TELEGRAM_API')
MEDIA_PATH = os.getenv('MEDIA_PATH')
MEDIA_URL = os.getenv('MEDIA_URL')
API_KEY = os.getenv('API_KEY')
# print(CHANNEL_ID)

# postgres
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


DATABASE_CONFIG = {
    "connections": {
        "default": f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        # "default": "sqlite://db.sqlite3" # for sqlite database, should be install `tortoise-orm[aSQLite]``
    },
    "apps": {
        "models": {
            "models": ["utils.db.models",  "aerich.models"],  
            "default_connection": "default",
        }
    }
}
