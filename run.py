import asyncio
import logging

from app.config import bot
from app.handlers import router
from aiogram import Bot, Dispatcher

async def main():
    dp = Dispatcher()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("\033[93mSomething went wrong trying to start bot! Try cheking out your .env file or bot token.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")