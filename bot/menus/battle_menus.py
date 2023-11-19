from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.dogemons import DOGEMONS
from bot.models.game import Game
from utils.utils import get_username_or_link


def waiting_battle_menu(user: types.User):
    text = f'{user.mention_html()} waiting for an opponent...'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Join', callback_data=f"join_battle_{user.id}")],
    ])

    return text, kb


def choose_battle_dogemon_menu(user: types.User, dogemons):
    user_link = user.mention_html()
    text = f'{user_link}, is ready for battle!\n\n' \
           f'Choose an dogeMON from the list below:'

    btns = []
    for dogemon in dogemons:
        btns.append([InlineKeyboardButton(text=f'Lvl. {dogemon["lvl"]} {dogemon["name"]}',
                                          callback_data=f'battle_dogeMON_{dogemon["name"]}')])

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *btns,
        [
            InlineKeyboardButton(text='🔙 Back', callback_data="main_menu"),
        ]
    ])

    return text, kb


def choose_dogemon1(user, game_id):
    # todo use user.mention_html()
    text = f'The first move is yours, @{user}, choose your dogeMON!'

    doge_btns = []
    for dogemon in DOGEMONS:
        doge_btns.append([
            InlineKeyboardButton(text=f'{dogemon["name"]}', callback_data=f"choose_dogemon|{game_id}|{dogemon['name']}"),
        ]),

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *doge_btns,
    ])

    return text, kb


def choose_dogemon2(user, game_id):
    # todo use user.mention_html()
    text = f'@{user} choose your dogeMON!'

    doge_btns = []
    for dogemon in DOGEMONS:
        doge_btns.append([
            InlineKeyboardButton(text=f'{dogemon["name"]}', callback_data=f"start_fight|{game_id}|{dogemon['name']}"),
        ]),

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *doge_btns,
    ])

    return text, kb


def choose_attack_menu(user: types.User, game):
    text = attack_text(user, game)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='⚔️Basic Atc.', callback_data=f"fight|basic_atc|{game.game_id}"),
            InlineKeyboardButton(text='☄️ Special Atc.', callback_data=f"fight|special_atc|{game.game_id}"),
        ],
        [
            InlineKeyboardButton(text='💫 Capture', callback_data=f"fight|capture_atc|{game.game_id}"),
            InlineKeyboardButton(text='🏃 Flee', callback_data=f"fight|flee|{game.game_id}"),
        ],
    ])

    return text, kb


def special_attack_menu(user, game):
    text = attack_text(user, game)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='☄️ Use Burn', callback_data="user_special_atc")],
        [InlineKeyboardButton(text='🔙 Back', callback_data=f"battle_dogeMON_{game.pokemon1.name}")],
    ])

    return text, kb


def attack_text(user, game: Game):
    user_link = user.mention_html()
    dogemon_text = f"<b>Lvl. {game.pokemon1.lvl} <i>{game.pokemon1.name}</i></b>\n" \
                   f"150/{game.pokemon1.hp}\n" \
                   f"100/{game.pokemon1.mp}"

    enemy_dogemon_text = f"<b>Lvl. {game.pokemon2.lvl} <i>{game.pokemon2.name}</i></b>\n" \
                         f"150/{game.pokemon2.hp}\n" \
                         f"100/{game.pokemon2.mp}"

    return f"{user_link} encountered a <b>Lvl. {game.pokemon2.lvl} <i>{game.pokemon2.name}</i></b> which is a <b>{game.pokemon2.type}</b> type dogeMON!\n\n" \
           f"⚔They've chosen to use <b><i>{game.pokemon1.name}</i> a Lvl. " \
           f"{game.pokemon2.lvl} <i>{game.pokemon2.name}</i></b>, which is a <b>{game.pokemon1.type}</b> type dogeMON!\n\n" \
           f"{dogemon_text}\n\n" \
           f"{enemy_dogemon_text}"
