import os
from datetime import date
from data.config import MEDIA_PATH

import aiohttp

from data.config import TELEGRAM_API, BOT_TOKEN


async def download_file(message, bot, save_path):
    if message.photo:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, save_path)
    elif message.document:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, save_path)
    return save_path
