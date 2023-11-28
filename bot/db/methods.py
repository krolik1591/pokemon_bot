from bson import ObjectId

from bot.db.db import mongodb

# USERS


async def create_new_user(user_id):
    await mongodb['users'].insert_one({
        'user_id': user_id,
        'balance': 100,
    })


async def is_user_exist(user_id):
    user = await mongodb['users'].find_one({'user_id': user_id})
    return bool(user)


# POKEMONS


async def create_new_pokemon(pokemon_info):
    await mongodb['pokemons'].insert_one(pokemon_info)


# GAME


async def create_new_game(game_info):
    game = await mongodb['games'].insert_one(game_info)
    return game.inserted_id


async def get_game_by_id(game_id):
    game_id = ObjectId(game_id)
    game = await mongodb['games'].find_one({'_id': game_id})
    return game


async def update_game(game_id, game_info):
    game_id = ObjectId(game_id)
    await mongodb['games'].update_one(
        {
            '_id': game_id
        },
        {
            '$set': game_info
        }
    )


# REWORK IT

async def get_user_balance(user_id):
    user = await mongodb['users'].find_one({'user_id': user_id})
    return user['balance']


if __name__ == '__main__':
    import asyncio
    async def main():
        x = await create_new_game({'1': 1, '2': 2})
        print(x)
    asyncio.run(main())
