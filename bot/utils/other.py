from bot.data.const import SPECIAL_EMOJI


def special_by_emoji(emoji: str) -> str:
    for special, emoji_ in SPECIAL_EMOJI.items():
        if emoji == emoji_:
            return special
