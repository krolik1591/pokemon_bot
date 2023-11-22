from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.models.game import Game
from bot.models.player import Player
from bot.models.pokemon_types import TYPE_STR
from bot.models.spell import Spell


def waiting_battle_menu(user: types.User):
    text = f'{user.mention_html()} waiting for an opponent...'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Join', callback_data=f"join_battle_{user.id}")],
    ])

    return text, kb


def select_dogemon_menu(game, first_move=False, latest_actions=None):
    def _pokemon_btn(pokemon_name):
        return InlineKeyboardButton(text=f'{pokemon_name}',
                                    callback_data=f"select_dogemon_menu|{game.game_id}|{pokemon_name}")

    player = game.who_move_player()
    actions_text = _actions_text(latest_actions)
    select_pok_text = f'The first move is yours, {player.mention}, choose your dogeMON!' \
        if first_move else f'{player.mention} choose your dogeMON!'

    text = f"{actions_text}\n\n{select_pok_text}"

    pokemons_btns = [_pokemon_btn(pokemon_name) for pokemon_name in player.pokemons_pool]
    pokemons_btns = _columns(pokemons_btns, 1)  # 1 column

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *pokemons_btns,
        _timeout_btn(game.game_id),
    ])

    return text, kb


def battle_menu(game, latest_actions=None):
    dogemon_text = _pokemon_text(game.player1)
    enemy_dogemon_text = _pokemon_text(game.player2)
    actions_text = _actions_text(latest_actions)

    player = game.who_move_player()

    text = f"{player.mention}, it's your turn to attack!\n\n" \
           f"{dogemon_text}\n\n" \
           f"{enemy_dogemon_text}\n\n" \
           f"{actions_text}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='⚔ Attack', callback_data=f"fight_menu|attack|{game.game_id}"),
            InlineKeyboardButton(text='☄️ Special Card.', callback_data=f"fight_menu|special_cards|{game.game_id}"),
        ],
        [
            InlineKeyboardButton(text='🏳️ Flee', callback_data=f"fight_menu|flee|{game.game_id}"),
            _timeout_btn(game.game_id),
        ],
    ])

    return text, kb


def select_attack_menu(game: Game):
    def _spell_btn(spell: Spell):
        spell_icon = '🛡' if spell.is_defence else f'{spell.attack}⚔'
        btn_text = f'{spell.name} ({spell_icon}) [x{spell.count}]'
        return InlineKeyboardButton(text=btn_text, callback_data=f"fight|{spell.name}|{game.game_id}")

    spells = game.who_move_player().pokemon.spells

    spell_btns = [_spell_btn(spell) for spell in spells]
    spell_btns = _columns(spell_btns, 2)  # two columns

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *spell_btns,
        [
            InlineKeyboardButton(text='🔙 Back', callback_data=f"select_dogemon|{game.game_id}|"),
            _timeout_btn(game.game_id),
        ]
    ])

    return kb


def _timeout_btn(game_id):
    return InlineKeyboardButton(text='⌛️ Timeout', callback_data=f"timeout|{game_id}"),


def _pokemon_text(player: Player):
    pokemon = player.pokemon
    shield_icon = "🛡" if pokemon.shield else ""

    return f"<b>Lvl. {pokemon.lvl} <i>{pokemon.name} {TYPE_STR[pokemon.type]} - {player.mention}</i></b>\n" \
           f"{_hp_bar(pokemon.hp, pokemon.max_hp)} {shield_icon}"


def _hp_bar(hp, max_hp):
    TOTAL_SYMBOLS = 10
    F1, F2, F3, EMPTY = "🟥", "🟧", "🟩", " .. "  # red yellow green empty

    hp_percent = hp / max_hp
    filled_symbols_count = round(TOTAL_SYMBOLS * hp_percent)
    empty_symbols_count = TOTAL_SYMBOLS - filled_symbols_count

    filled_symbol = F1
    if hp_percent > 0.3:
        filled_symbol = F2
    if hp_percent > 0.6:
        filled_symbol = F3

    bar = filled_symbol * filled_symbols_count + EMPTY * empty_symbols_count

    return f"HP: [{bar}] {hp} / {max_hp}"


def _actions_text(actions: [str]):
    if actions is None:
        return ""
    return '\n'.join(actions)


def _columns(arr, chunk_size):
    return [arr[i:i + chunk_size]
            for i in range(0, len(arr), chunk_size)]
