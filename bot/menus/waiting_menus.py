from aiogram.types import User, InlineKeyboardMarkup, InlineKeyboardButton


def waiting_battle_menu(user: User, bet):
    text = f'{user.mention_html()} waiting for an opponent...'
    if bet:
        text += f'\n\nBet: {bet}'
    else:
        text += '\n\nNo bet'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Join', callback_data=f"join_battle|{user.id}|{bet}"),
            InlineKeyboardButton(text='Cancel', callback_data=f"cancel_battle|{user.id}")],
    ])

    return text, kb


def waiting_group_battle_menu(bet, players):
    text_blue = 'Blue team:\n'
    text_red = 'Red team:\n'
    for blue_player in players['blue']:
        text_blue += f"     {blue_player.mention_html()}\n"
    for red_player in players['red']:
        text_red += f"     {red_player.mention_html()}\n"

    text = f'{text_blue}\n{text_red}\n\nBet: {bet}'

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Join BLUE ({len(players["blue"])}/2)', callback_data=f"group_battle|{bet}|blue"),
            InlineKeyboardButton(text=f'Join RED ({len(players["red"])}/2)', callback_data=f"group_battle|{bet}|red"),

        ],
        [InlineKeyboardButton(text='Cancel', callback_data=f"cancel_battle|{players['blue'][0].id}")],
    ])

    return text, kb