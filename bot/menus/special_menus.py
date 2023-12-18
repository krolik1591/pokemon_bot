from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.data.const import SPECIAL_EMOJI, IS_DONATE_EMOJI
from bot.data.dogemons import DOGEMONS_MAP
from bot.menus.utils_for_menus import set_callback_special, _inline_btn, _timeout_btn, _pokemon_text_small
from bot.models.game import Game


def special_cards_menu(game: Game, donate_special: list):
    attacker, defender = game.get_attacker_defencer_team()
    defender_index = game.players.index(defender[0]) if len(game.players) == 2 else None

    print('')
    special_btns = []
    if len(attacker[0].special_cards) == 1:
        text = f"{SPECIAL_EMOJI[attacker[0].special_cards[0]]} {attacker[0].special_cards[0]}"
        callback_data = set_callback_special(game, SPECIAL_EMOJI[attacker[0].special_cards[0]], defender_index, is_donate=False)
        special_btns.append(_inline_btn(text, callback_data))

    for index, special_card in enumerate(donate_special):
        text = f"{SPECIAL_EMOJI[special_card]} {special_card} {IS_DONATE_EMOJI}"
        callback_data = set_callback_special(game, SPECIAL_EMOJI[special_card], defender_index, is_donate=True)
        special_btns.append(_inline_btn(text, callback_data))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *special_btns,
        [
            InlineKeyboardButton(text='🔙 Back', callback_data=f"select_dogemon_menu|None|{game.game_id}|False"),
            _timeout_btn(game.game_id),
        ],
    ])

    return kb


def revive_pokemon_menu(game: Game, pokemons_to_revive, is_donate):
    text = 'Select pokemon to revive:'

    if is_donate:
        # ... is_special ....special_card_target
        revive_btns = [
            InlineKeyboardButton(text=_pokemon_text_small(DOGEMONS_MAP[pokemon_name], is_link=True),
                                 callback_data=f"fight|T|{pokemon_name}{IS_DONATE_EMOJI}|{game.game_id}|None")
            for pokemon_name in pokemons_to_revive
        ]
    else:
        revive_btns = [
            InlineKeyboardButton(text=_pokemon_text_small(DOGEMONS_MAP[pokemon_name], is_link=True),
                                 callback_data=f"fight|T|{pokemon_name}|{game.game_id}|None")
            for pokemon_name in pokemons_to_revive
        ]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        revive_btns,
        [
            InlineKeyboardButton(text='🔙 Back', callback_data=f"select_dogemon_menu|None|{game.game_id}|False"),
            _timeout_btn(game.game_id),
        ],
    ])

    return text, kb