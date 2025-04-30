import asyncio
from handlers.users import start, find_udk
from callbaks import pagination
from middlewares.throttling import ThrottlingMiddleware
from utils.bot_stop import on_shutdown_notify
from utils.set_bot_commands import (
    set_private_default_commands
)
from utils.bot_start import on_startup_notify
from loader import bot, dp, init_db


async def main():
    await init_db()  

    dp.message.middleware(ThrottlingMiddleware())

    dp.include_routers(
        start.router,
        find_udk.router,
        pagination.router,
    )

    await set_private_default_commands(bot)
    await on_startup_notify()

    await bot.delete_webhook(drop_pending_updates=False)

    try:
        await dp.start_polling(bot, skip_updates=True)
    except asyncio.CancelledError:
        pass
    finally:
        await on_shutdown_notify()  

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🚀 Bot o‘chirildi.")
