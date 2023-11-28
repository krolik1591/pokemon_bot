from motor.motor_asyncio import AsyncIOMotorClient

from bot.utils.config_reader import config

mongodb = AsyncIOMotorClient(config.mongo_connection_string)["PokemonBot"]


if __name__ == '__main__':
    pass