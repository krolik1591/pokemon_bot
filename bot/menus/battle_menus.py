from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, User

from bot.data.const import REVIVE, IS_DONATE_EMOJI
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


def waiting_group_battle_menu(bet, players):
    text_blue = 'Blue team:\n'
    text_red = 'Red team:\n'
    for blue_player in players['blue']:
        text_blue += f"     {blue_player.mention_html()}\n"
    for red_player in players['red']:
        text_red += f"     {red_player.mention_html()}\n"

    text = f'{text_blue}\n{text_red}\n\nBet: {bet}'

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Join BLUE ({len(players["blue"])}/2)', callback_data=f"group_battle|{bet}|blue"),
            InlineKeyboardButton(text=f'Join RED ({len(players["red"])}/2)', callback_data=f"group_battle|{bet}|red"),

        ],
        [InlineKeyboardButton(text='Cancel', callback_data=f"cancel_battle|{players['blue'][0].id}")],
    ])

    return text, kb


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


def _inline_btn(text, callback_data):
    return [InlineKeyboardButton(text=text, callback_data=callback_data)]


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
