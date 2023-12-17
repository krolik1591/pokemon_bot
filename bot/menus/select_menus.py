from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.data.dogemons import DOGEMONS_MAP
from bot.menus.utils_for_menus import _inline_btn, _timeout_btn, _pokemon_text_small, _actions_text, _columns
from bot.models.game import Game
from bot.models.spell import Spell


def select_dogemon_menu(game, first_move=False, latest_actions=None, change_first_move=False):
    def _pokemon_btn(pokemon_name):
        btn_text = _pokemon_text_small(DOGEMONS_MAP[pokemon_name], is_link=True)
        return InlineKeyboardButton(text=btn_text,
                                    callback_data=f"select_dogemon_menu|{pokemon_name}|{game.game_id}|{change_first_move}")

    attacker = game.get_attacker()

    actions_text = _actions_text(latest_actions)
    select_pok_text = f'The first move is yours, {attacker.mention}, choose your PokéCard!' \
        if first_move else f'{attacker.mention} choose your PokéCard!'

    attacker_team, defender_team = game.get_attacker_defencer_team()
    other_players = game.players
    other_players_text = []
    for player in other_players:
        if player.pokemon:
            other_players_text.append(f"🔶{player.name} plays as: {_pokemon_text_small(player.pokemon)}\n")
        else:
            other_players_text.append(f"🔶{player.name} plays as: waiting...\n")

    text = f"{actions_text}\n\n{''.join(other_players_text)}\n{select_pok_text}"

    pokemons_btns = [_pokemon_btn(pokemon_name) for pokemon_name, is_alive in attacker.pokemons_pool.items() if
                     is_alive]
    pokemons_btns = _columns(pokemons_btns, 1)  # 1 column

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *pokemons_btns,
        [_timeout_btn(game.game_id)],
    ])

    return text, kb


def select_defender_menu(game: Game, item_name, is_special: str):
    print('select_defender_menu')
    attacker_team, defender_team = game.get_attacker_defencer_team()

    # actions_text = _actions_text(latest_actions)
    # text = f"{actions_text}\n\n"
    # text = f"{attacker_team[0].mention}, choose your target!"

    defenders_btns = []
    for defender in defender_team:
        defender_index = game.players.index(defender_team[0])
        text = f"{defender.name} ({_pokemon_text_small(defender.pokemon, is_link=True)})\n"
        callback_data = f"fight|{is_special}|{item_name}|{game.game_id}|F|{defender_index}"
        defenders_btns.append(_inline_btn(text, callback_data))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *defenders_btns,
        [
            InlineKeyboardButton(text='🔙 Back', callback_data=f"select_dogemon_menu|None|{game.game_id}|False"),
            _timeout_btn(game.game_id)],
    ])

    return kb


def select_attack_menu(game: Game):
    attacker_team, defender_team = game.get_attacker_defencer_team()

    if len(game.players) == 2:
        defender_index = game.players.index(defender_team[0])
    else:
        defender_index = None

    def _spell_btn(spell: Spell):
        spell_icon = '🛡' if spell.is_defence else f'{spell.attack}⚔'
        btn_text = f'{spell.name} ({spell_icon}) [x{spell.count}]'
        # ... is_special ..... is_revive
        return InlineKeyboardButton(text=btn_text,
                                    callback_data=f"fight|F|{spell.name}|{game.game_id}|F|{defender_index}")

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