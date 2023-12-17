from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.data.const import IS_DONATE_EMOJI
from bot.data.dogemons import DOGEMONS_MAP
from bot.menus.utils_for_menus import set_callback_special, _inline_btn, _timeout_btn, _flee_btn, _pokemon_text, \
    _pokemon_text_small, _actions_text
from bot.models.game import Game


def battle_menu(game: Game, latest_actions=None):
    players_text = []
    for player in game.players:
        if player.pokemon:
            players_text.append(_pokemon_text(player))
    players_text = '\n\n'.join(players_text)
    actions_text = _actions_text(latest_actions)

    player = game.get_attacker()

    text = f"{player.mention}, it's your turn to attack!\n\n" \
           f"{players_text}\n\n" \
           f"{actions_text}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Now attacks: {player.name}", callback_data="nothing"),
        ],
        [
            InlineKeyboardButton(text='⚔ Attack', callback_data=f"fight_menu|attack|{game.game_id}"),
            InlineKeyboardButton(text='🎒 PokéBag', callback_data=f"fight_menu|special_cards|{game.game_id}"),
        ],
        [
            _timeout_btn(game.game_id),
            _flee_btn(game.game_id),
        ],
    ])

    return text, kb


def special_cards_menu(game: Game, donate_special: list):
    attacker, defender = game.get_attacker_defencer_team()
    defender_index = game.players.index(defender[0]) if len(game.players) == 2 else None

    special_btns = []
    if len(attacker[0].special_cards) == 1:
        callback_data = set_callback_special(game, attacker[0].special_cards[0], defender_index, is_donate=False)
        special_btns.append(_inline_btn(attacker[0].special_cards[0], callback_data))

    for index, special_card in enumerate(donate_special):
        text = special_card + ' 💵'
        callback_data = set_callback_special(game, special_card, defender_index, is_donate=True)
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
        # ... is_special ..... is_revive|special_card_target
        revive_btns = [
            InlineKeyboardButton(text=_pokemon_text_small(DOGEMONS_MAP[pokemon_name], is_link=True),
                                 callback_data=f"fight|T|{pokemon_name}{IS_DONATE_EMOJI}|{game.game_id}|T|None")
            for pokemon_name in pokemons_to_revive
        ]
    else:
        revive_btns = [
            InlineKeyboardButton(text=_pokemon_text_small(DOGEMONS_MAP[pokemon_name], is_link=True),
                                 callback_data=f"fight|T|{pokemon_name}|{game.game_id}|T|None")
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
