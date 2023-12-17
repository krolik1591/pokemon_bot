from aiogram.types import InlineKeyboardButton

from bot.data.const import REVIVE, IS_DONATE_EMOJI
from bot.models.player import Player
from bot.models.pokemon_types import TYPES_STR
from bot.utils.hp_bar import hp_bar


def _pokemon_text(player: Player):
    pokemon = player.pokemon
    link = f"<a href='{pokemon.url}'>{pokemon.name}</a>"
    shield_icon = "🛡" if pokemon.shield else ""
    sleeping_pills_icon = "💤" if player.sleeping_pills_counter is not None else ""
    power_increase_icon = "🔥" if pokemon.increase_dmg_by_card else ""

    return f"<b>Lvl. {pokemon.lvl} {link} {TYPES_STR[pokemon.type]} - {player.mention}</b>\n" \
           f"{hp_bar(pokemon.hp, pokemon.max_hp)} {power_increase_icon} {shield_icon} {sleeping_pills_icon}"


def set_callback_special(game, special_card, defender_index, is_donate):
    if is_donate:
        if special_card == REVIVE:
            callback_data = f"revive_pokemon{IS_DONATE_EMOJI}|{game.game_id}"
        else:
            # ... is_special ..... is_revive
            callback_data = f"fight|T|{special_card}{IS_DONATE_EMOJI}|{game.game_id}|F|{defender_index}"

    else:
        if special_card == REVIVE:
            callback_data = f"revive_pokemon|{game.game_id}"
        else:
            callback_data = f"fight|T|{special_card}|{game.game_id}|F|{defender_index}"

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