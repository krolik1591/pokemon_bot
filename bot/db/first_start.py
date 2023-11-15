from bot.db import db
from bot.db.db import mongodb


async def mongo_first_start():
    is_exist = await mongodb.list_collection_names()
    if is_exist:
        return

    print('First start, creating collections...')

    collection_names = ['users', 'pokemons', 'gamelogs']

    for collection_name in collection_names:
        await mongodb.create_collection(collection_name)

    mongodb['users'].create_index('user_id', unique=True)
    mongodb['pokemons'].create_index('name', unique=True)
