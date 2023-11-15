from aiogram import types


def get_username_or_link(user: types.User):
    return user.mention_html()
