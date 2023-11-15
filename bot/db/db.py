from motor.motor_asyncio import AsyncIOMotorClient

from utils.config_reader import config

mongodb = AsyncIOMotorClient(config.mongo_connection_string)["PokemonBot"]


if __name__ == '__main__':
    print(config.mongo_connection_string)
