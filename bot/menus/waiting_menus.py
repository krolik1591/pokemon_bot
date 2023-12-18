from aiogram.types import User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link


def waiting_battle_menu(user: User, bet):
    text = f'{user.mention_html()} waiting for an opponent...'
    if bet:
        text += f'\n\nBet: {bet}'
    else:
        text += '\n\nNo bet'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Join', callback_data=f"join_battle|{user.id}|{bet}"),
            InlineKeyboardButton(text='Cancel', callback_data=f"cancel_battle|{user.id}|1x1")],
    ])

    return text, kb


def waiting_group_battle_menu(bet, players, pre_battle_id):
    text_blue = '🔹 Blue team:\n'
    text_red = '🔸 Yellow team:\n'
    for blue_player_id in players['blue']:
        link = markdown.hlink(players[str(blue_player_id)], create_tg_link("user", id=blue_player_id))
        text_blue += f"        {link}\n"
    for red_player_id in players['red']:
        link = markdown.hlink(players[str(red_player_id)], create_tg_link("user", id=red_player_id))
        text_red += f"         {link}\n"

    text = f'{text_blue}\n{text_red}\n\nBet: {bet}'

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Join BLUE ({len(players["blue"])}/2)', callback_data=f"group_battle|{bet}|blue|{pre_battle_id}"),
            InlineKeyboardButton(text=f'Join YELLOW ({len(players["red"])}/2)', callback_data=f"group_battle|{bet}|red|{pre_battle_id}"),

        ],
        [InlineKeyboardButton(text='Cancel', callback_data=f"cancel_battle|{players['blue'][0]}|{pre_battle_id}")],
    ])

    return text, kb
