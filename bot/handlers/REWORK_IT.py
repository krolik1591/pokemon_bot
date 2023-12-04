from bot.db import methods as db
from bot.models.game import Game


async def pre_game_check(player_id, bet, without_bets=False):
    active_game = await db.get_active_game(player_id)
    if active_game:
        return f'You are already in game!'

    if without_bets or bet is None:
        return None

    user1_balance = await db.get_user_balance(player_id)
    if user1_balance < bet:
        return f'You have no money to bet!'

    return None


async def take_money_from_players(player1_id, player2_id, bet):
    await db.withdraw_tokens(player1_id, bet)
    await db.withdraw_tokens(player2_id, bet)


async def end_game(winner_id, game: Game):
    await db.update_game(game.game_id, {'winner': winner_id})

    if game.bet is None:
        return
    for_winner = game.bet * 2 * 0.95
    prize_pool = game.bet * 2 * 0.05

    await db.deposit_tokens(winner_id, for_winner)
    await db.deposit_burn(prize_pool)
