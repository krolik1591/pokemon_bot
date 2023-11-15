from bot.db.db import mongodb

# USERS


async def create_new_user(user_id):
    await mongodb['users'].insert_one({
        'user_id': user_id,
    })


async def is_user_exist(user_id):
    user = await mongodb['users'].find_one({'user_id': user_id})
    return bool(user)


# POKEMONS


async def create_new_pokemon(pokemon_info):
    await mongodb['pokemons'].insert_one(pokemon_info)


# GAME


async def create_new_game(game_info):
    await mongodb['games'].insert_one(game_info)


if __name__ == '__main__':
    import asyncio
    async def main():
        await create_new_user(1)
    asyncio.run(main())
