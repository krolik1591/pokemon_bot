from bot.db import methods as db


async def pre_game_check(player_id, bet):
    active_game = await db.get_active_game(player_id)
    if active_game:
        return f'You are already in game!'

    user1_balance = await db.get_user_balance(player_id)
    if user1_balance < bet:
        return f'You have no money to bet!'

    return None


async def take_money_from_players(player1_id, player2_id, bet):
    await db.update_user_balance(player1_id, -bet)
    await db.update_user_balance(player2_id, -bet)
