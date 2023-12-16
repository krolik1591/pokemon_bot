from motor.motor_asyncio import AsyncIOMotorClient

from bot.utils.config_reader import config

mongodb = AsyncIOMotorClient(config.mongo_connection_string)["PokemonBotTesting"]


if __name__ == '__main__':
    import asyncio

    async def test():
        print(await mongodb.list_collection_names())

    asyncio.run(test())
