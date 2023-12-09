from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, User

from bot.data.const import REVIVE
from bot.data.dogemons import DOGEMONS_MAP
from bot.models.game import Game
from bot.models.player import Player
from bot.models.pokemon_types import TYPES_STR
from bot.models.spell import Spell
from bot.utils.hp_bar import hp_bar


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


def select_dogemon_menu(game, first_move=False, latest_actions=None, change_first_move=False):
    def _pokemon_btn(pokemon_name):
        btn_text = _pokemon_text_small(DOGEMONS_MAP[pokemon_name], is_link=True)
        return InlineKeyboardButton(text=btn_text,
                                    callback_data=f"select_dogemon_menu|{pokemon_name}|{game.game_id}|{change_first_move}")

    player, opponent = game.get_attacker_defencer()

    actions_text = _actions_text(latest_actions)
    select_pok_text = f'The first move is yours, {player.mention}, choose your dogeMON!' \
        if first_move else f'{player.mention} choose your dogeMON!'
    opponents_pokemon = f"🔶{opponent.name} plays as: {_pokemon_text_small(opponent.pokemon)}\n" if opponent.pokemon else ""

    text = f"{actions_text}\n\n{opponents_pokemon}\n{select_pok_text}"

    pokemons_btns = [_pokemon_btn(pokemon_name) for pokemon_name, is_alive in player.pokemons_pool.items() if is_alive]
    pokemons_btns = _columns(pokemons_btns, 1)  # 1 column

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *pokemons_btns,
        [_timeout_btn(game.game_id)],
    ])

    return text, kb


def battle_menu(game: Game, latest_actions=None):
    dogemon_text = _pokemon_text(game.player1)
    enemy_dogemon_text = _pokemon_text(game.player2)
    actions_text = _actions_text(latest_actions)

    player = game.get_attacker()

    text = f"{player.mention}, it's your turn to attack!\n\n" \
           f"{dogemon_text}\n\n" \
           f"{enemy_dogemon_text}\n\n" \
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


def select_attack_menu(game: Game):
    def _spell_btn(spell: Spell):
        spell_icon = '🛡' if spell.is_defence else f'{spell.attack}⚔'
        btn_text = f'{spell.name} ({spell_icon}) [x{spell.count}]'
        return InlineKeyboardButton(text=btn_text, callback_data=f"fight|{False}|{spell.name}|{game.game_id}")

    spells = game.get_attacker().pokemon.spells

    spell_btns = [_spell_btn(spell) for spell in spells]
    spell_btns = _columns(spell_btns, 1)  # two columns

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *spell_btns,
        [
            InlineKeyboardButton(text='🔙 Back', callback_data=f"select_dogemon_menu|None|{game.game_id}|False"),
            _timeout_btn(game.game_id),
        ]
    ])

    return kb


def special_cards_menu(game: Game):
    player = game.get_attacker()

    if player.special_card == REVIVE:
        callback_data = f"revive_pokemon|{game.game_id}"
    else:
        callback_data = f"fight|True|{player.special_card}|{game.game_id}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f'{player.special_card}', callback_data=callback_data),
        ],
        [
            InlineKeyboardButton(text='🔙 Back', callback_data=f"select_dogemon_menu|None|{game.game_id}|False"),
            _timeout_btn(game.game_id),
        ],
    ])

    return kb


def revive_pokemon_menu(game: Game, pokemons_to_revive):
    text = 'Select pokemon to revive:'

    revive_btns = [
        InlineKeyboardButton(text=_pokemon_text_small(DOGEMONS_MAP[pokemon_name], is_link=True),
                             callback_data=f"fight|True|{pokemon_name}|{game.game_id}")
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


def _timeout_btn(game_id):
    return InlineKeyboardButton(text='⌛️ Timeout', callback_data=f"timeout|{game_id}")


def _flee_btn(game_id):
    return InlineKeyboardButton(text='️🏃 Flee', callback_data=f"fight_menu|flee|{game_id}")


def _pokemon_text(player: Player):
    pokemon = player.pokemon
    link = f"<a href='{pokemon.url}'>{pokemon.name}</a>"
    shield_icon = "🛡" if pokemon.shield else ""
    sleeping_pills_icon = "💤" if player.sleeping_pills_counter is not None else ""
    power_increase_icon = "🔥" if pokemon.increase_dmg_by_card else ""

    return f"<b>Lvl. {pokemon.lvl} {link} {TYPES_STR[pokemon.type]} - {player.mention}</b>\n" \
           f"{hp_bar(pokemon.hp, pokemon.max_hp)} {power_increase_icon} {shield_icon} {sleeping_pills_icon}"


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
