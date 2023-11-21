import random

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.dogemons import DOGEMONS
from bot.models.game import Game
from bot.models.player import Player
from bot.models.pokemon import Pokemon
from utils.utils import get_username_or_link

POKEMON_TYPE = {
    'Fire': '🔥',
    'Water': '💧',
    'Grass': '🌱',
    'Earth': '🌎',
    'Air': '💨',
    'Electric': '⚡️',
}


def waiting_battle_menu(user: types.User):
    text = f'{user.mention_html()} waiting for an opponent...'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Join', callback_data=f"join_battle_{user.id}")],
    ])

    return text, kb


def choose_dogemon(game, first_move=False, callback='choose_dogemon'):
    player, _ = game.who_move_tg_id_pokemon()

    if first_move:
        text = f'The first move is yours, {player.mention}, choose your dogeMON!'
    else:
        text = f'{player.mention} choose your dogeMON!'

    doge_btns = []

    for dogemon_name in player.pokemons_pool:
        doge_btns.append([
            InlineKeyboardButton(text=f'{dogemon_name}',
                                 callback_data=f"{callback}|{game.game_id}|{dogemon_name}"),
        ]),

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *doge_btns,
    ])

    return text, kb


def choose_attack_menu(game):
    text = attack_text(game)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='⚔️Basic Atc.', callback_data=f"fight|basic_atc|{game.game_id}"),
            InlineKeyboardButton(text='☄️ Special Atc.', callback_data=f"fight|special_atc|{game.game_id}"),
        ],
        [
            InlineKeyboardButton(text='👊 Power Atc.', callback_data=f"fight|power_atk|{game.game_id}"),
            InlineKeyboardButton(text='🀄️ Special Card', callback_data=f"fight|flee|{game.game_id}"),
        ],
    ])

    return text, kb


def special_attack_menu(game):
    text = attack_text(game)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='☄️ Use Burn', callback_data="user_special_atc")],
        [InlineKeyboardButton(text='🔙 Back', callback_data=f"battle_dogeMON_{game.pokemon1.name}")],
    ])

    return text, kb


def attack_text(game: Game):
    dogemon_text = _pokemon_text(game.pokemon1, game.player1)
    enemy_dogemon_text = _pokemon_text(game.pokemon2, game.player2)

    player, _ = game.who_move_tg_id_pokemon()
    return f"{player.mention}, it's your turn to attack!\n\n" \
           f"{dogemon_text}\n\n" \
           f"{enemy_dogemon_text}"


def _pokemon_text(pokemon: Pokemon, player: Player):
    return f"<b>Lvl. {pokemon.lvl} <i>{pokemon.name} {POKEMON_TYPE[pokemon.type]} - {player.mention}</i></b>\n" \
           f"🟥{pokemon.hp}/{pokemon.max_hp}\n" \
           f"🟦{pokemon.mp}/{pokemon.max_mp}"
