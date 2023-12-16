from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link

from bot.data.const import MAX_ACTIVE_GAMES, REWARD, PRIZE_POOL
from bot.db import methods as db
from bot.models.game import Game


async def pre_game_check(player, bet, without_bets=False):
    active_games = await db.get_active_games(player.id)
    if len(active_games) >= MAX_ACTIVE_GAMES:
        game_ids = [f"<code>{str(game['_id'])}</code>" for game in active_games]
        return f'{player.mention} have {len(active_games)} games.\n' \
               f'Game ids: \n{", ".join(game_ids)}\n\n' \
               f'Maximum active games: {MAX_ACTIVE_GAMES}\n\n'

    if without_bets or bet is None:
        return None

    user1_balance = await db.get_user_balance(player.id)
    if user1_balance < bet:
        return f"Sorry you don't have tokens to start a battle!"

    return None


async def take_money_from_players(player1_id, player2_id, bet):
    await db.withdraw_tokens(player1_id, bet)
    await db.withdraw_tokens(player2_id, bet)


async def end_game(winners_id: [], game: Game):
    await db.update_game(game.game_id, {'winner': winners_id})

    if game.bet is None:
        return
    for_winner = game.bet * 2 * REWARD
    prize_pool = game.bet * 2 * PRIZE_POOL

    await db.deposit_tokens(winners_id, for_winner)
    await db.deposit_burn(prize_pool)
