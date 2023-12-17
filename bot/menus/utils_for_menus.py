from aiogram.types import InlineKeyboardButton

from bot.data.const import REVIVE, IS_DONATE_EMOJI, SPECIAL_EMOJI
from bot.models.pokemon_types import TYPES_STR


def set_callback_special(game, special_card_emoji, defender_index, is_donate):
    if is_donate:
        if special_card_emoji == SPECIAL_EMOJI[REVIVE]:
            callback_data = f"revive_pokemon{IS_DONATE_EMOJI}|{game.game_id}"
        else:
            # ... is_special ..... is_revive
            callback_data = f"fight|T|{special_card_emoji}{IS_DONATE_EMOJI}|{game.game_id}|{defender_index}"

    else:
        if special_card_emoji == SPECIAL_EMOJI[REVIVE]:
            callback_data = f"revive_pokemon|{game.game_id}"
        else:
            callback_data = f"fight|T|{special_card_emoji}|{game.game_id}|{defender_index}"

    return callback_data


def _inline_btn(text, callback_data):
    return [InlineKeyboardButton(text=text, callback_data=callback_data)]


def _timeout_btn(game_id):
    return InlineKeyboardButton(text='⌛️ Timeout', callback_data=f"timeout|{game_id}")


def _flee_btn(game_id):
    return InlineKeyboardButton(text='️🏃 Flee', callback_data=f"fight_menu|flee|{game_id}")


def _pokemon_text_small(pokemon, is_link=False):
    link = f"<a href='{pokemon.url}'>{pokemon.name}</a>" if not is_link else pokemon.name
    return f"Lvl {pokemon.lvl} {link} {TYPES_STR[pokemon.type]}"


def _actions_text(actions: [str]):
    if actions is None:
        return ""
    return '\n'.join([f"🔹{a}" for a in actions])


def _columns(arr, chunk_size):
    return [arr[i:i + chunk_size]
            for i in range(0, len(arr), chunk_size)]