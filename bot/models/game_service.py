from bot.db import db
from bot.models.game import Game


async def get_game(game_id):
    game_json = await db.get_game_by_id(game_id)
    return Game.from_mongo(game_json)


async def save_game(game: Game):
    if game.game_id is None:
        game.game_id = await db.create_new_game(game.to_mongo())
    else:
        await db.update_game(game.game_id, game.to_mongo())

    return game

