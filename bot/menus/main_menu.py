from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(user: types.User):
    user_link = user.mention_html()

    text = f'Hi, {user_link}, and welcome to dogeMON!'
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='💰 Shop', callback_data="shop_menu"),
            InlineKeyboardButton(text='🔥 Battle', callback_data="choose_battle_dogemon_menu"),
        ],
        [
            InlineKeyboardButton(text='🗺 Travel', callback_data="travel_menu"),
            InlineKeyboardButton(text='🏙 Area', callback_data="area_menu"),
        ],
        [
            InlineKeyboardButton(text='🐶 Your dogeMON', callback_data="pokemon_menu"),
            InlineKeyboardButton(text='👨‍🦰 Your Profile', callback_data="profile_menu"),
        ],
    ])
    return kb
