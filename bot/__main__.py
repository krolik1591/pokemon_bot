import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot.db.first_start import mongo_first_start
from bot.handlers import routers
from bot.utils.config_reader import config


async def main(bot, dp):
    logging.basicConfig(level=logging.WARNING)

    for router in routers:
        dp.include_router(router)

    await set_bot_commands(bot)

    await mongo_first_start()

    try:
        print("me:", await bot.me())
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command="start", description="Pokemon menu "),
    ], scope=types.BotCommandScopeAllPrivateChats())

    await bot.set_my_commands(commands=[
        types.BotCommand(command="battle", description="Start battle"),
    ], scope=types.BotCommandScopeAllGroupChats())


if __name__ == '__main__':
    if config.fsm_mode == "redis":
        storage = RedisStorage.from_url(url=config.redis, connection_kwargs={"decode_responses": True})
    else:
        storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    asyncio.run(main(bot, dp))
