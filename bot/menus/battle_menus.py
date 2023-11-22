from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.models.game import Game
from bot.models.player import Player
from bot.models.pokemon_types import TYPE_STR


def waiting_battle_menu(user: types.User):
    text = f'{user.mention_html()} waiting for an opponent...'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Join', callback_data=f"join_battle_{user.id}")],
    ])

    return text, kb


def choose_dogemon(game, first_move=False):
    player = game.who_move_player()

    if first_move:
        text = f'The first move is yours, {player.mention}, choose your dogeMON!'
    else:
        text = f'{player.mention} choose your dogeMON!'

    doge_btns = []

    for dogemon_name in player.pokemons_pool:
        doge_btns.append([
            InlineKeyboardButton(text=f'{dogemon_name}',
                                 callback_data=f"choose_dogemon|{game.game_id}|{dogemon_name}"),
        ]),

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *doge_btns,
    ])

    return text, kb


def battle_menu(game):
    text = attack_text(game)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='⚔ Attack', callback_data=f"fight_menu|attack|{game.game_id}"),
            InlineKeyboardButton(text='☄️ Special Card.', callback_data=f"fight_menu|special_cards|{game.game_id}"),
        ],
        [
            InlineKeyboardButton(text='⌛️ Timeout', callback_data=f"timeout|{game.game_id}"),
            InlineKeyboardButton(text='🏳️ Flee', callback_data=f"fight_menu|flee|{game.game_id}"),
        ],
    ])

    return text, kb


def select_attack(game: Game):
    text = attack_text(game)

    player = game.who_move_player()
    btns = []
    btn_row = []
    for spell in player.pokemon.spells:
        btn_row.append(
            InlineKeyboardButton(text=f'{spell.name} ({spell.attack}⚔️)',
                                 callback_data=f"fight|{spell.name}|{game.game_id}"),
        )
        if len(btn_row) == 2:
            btns.append(btn_row)
            btn_row = []

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *btns,
        [
            InlineKeyboardButton(text='⌛️ Timeout', callback_data=f"timeout|{game.game_id}"),
            InlineKeyboardButton(text='🔙 Back', callback_data=f"choose_dogemon|{game.game_id}|"),
        ]
    ])

    return text, kb


def attack_text(game: Game):
    dogemon_text = _pokemon_text(game.player1)
    enemy_dogemon_text = _pokemon_text(game.player2)

    player = game.who_move_player()
    return f"{player.mention}, it's your turn to attack!\n\n" \
           f"{dogemon_text}\n\n" \
           f"{enemy_dogemon_text}"


def _pokemon_text(player: Player):
    pokemon = player.pokemon
    return f"<b>Lvl. {pokemon.lvl} <i>{pokemon.name} {TYPE_STR[pokemon.type]} - {player.mention}</i></b>\n" \
           f"{hp_bar(pokemon.hp, pokemon.max_hp)}\n"


def hp_bar(hp, max_hp):
    TOTAL_SYMBOLS = 10
    FILLED, EMPTY = "🟥", " .. "

    filled_symbols = round(TOTAL_SYMBOLS * hp / max_hp)
    empty_symbols = TOTAL_SYMBOLS - filled_symbols
    bar = FILLED * filled_symbols + EMPTY * empty_symbols

    return f"HP: [{bar}] {hp} / {max_hp}"
