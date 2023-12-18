from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link

from bot.data.const import SPECIAL_EMOJI


def special_by_emoji(emoji: str) -> str:
    for special, emoji_ in SPECIAL_EMOJI.items():
        if emoji == emoji_:
            return special


def get_mention(user_id: int, name: str) -> str:
    return markdown.hlink(name, create_tg_link("user", id=user_id))
