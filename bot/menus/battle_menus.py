from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, User

from bot.models import Game, Player, TYPES_STR, Spell
from bot.utils.hp_bar import hp_bar


def waiting_battle_menu(user: User):
    text = f'{user.mention_html()} waiting for an opponent...'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Join', callback_data=f"join_battle_{user.id}")],
    ])

    return text, kb


def select_dogemon_menu(game, first_move=False, latest_actions=None):
    def _pokemon_btn(pokemon_name):
        return InlineKeyboardButton(text=pokemon_name,
                                    callback_data=f"select_dogemon_menu|{game.game_id}|{pokemon_name}")

    player = game.get_attacker()
    actions_text = _actions_text(latest_actions)
    select_pok_text = f'The first move is yours, {player.mention}, choose your dogeMON!' \
        if first_move else f'{player.mention} choose your dogeMON!'

    text = f"{actions_text}\n\n{select_pok_text}"

    pokemons_btns = [_pokemon_btn(pokemon_name) for pokemon_name, is_alive in player.pokemons_pool.items() if is_alive]
    pokemons_btns = _columns(pokemons_btns, 1)  # 1 column

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *pokemons_btns,
        _timeout_btn(game.game_id),
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
            InlineKeyboardButton(text='⚔ Attack', callback_data=f"fight_menu|attack|{game.game_id}"),
            InlineKeyboardButton(text='☄️ Special Card.', callback_data=f"fight_menu|special_cards|{game.game_id}"),
        ],
        [
            InlineKeyboardButton(text='🏳️ Flee', callback_data=f"fight_menu|flee|{game.game_id}"),
            *_timeout_btn(game.game_id),
        ],
    ])

    return text, kb


def select_attack_menu(game: Game):
    def _spell_btn(spell: Spell):
        spell_icon = '🛡' if spell.is_defence else f'{spell.attack}⚔'
        btn_text = f'{spell.name} ({spell_icon}) [x{spell.count}]'
        return InlineKeyboardButton(text=btn_text, callback_data=f"fight|{spell.name}|{game.game_id}")

    spells = game.get_attacker().pokemon.spells

    spell_btns = [_spell_btn(spell) for spell in spells]
    spell_btns = _columns(spell_btns, 2)  # two columns

    kb = InlineKeyboardMarkup(inline_keyboard=[
        *spell_btns,
        [
            InlineKeyboardButton(text='🔙 Back', callback_data=f"select_dogemon|{game.game_id}|"),
            *_timeout_btn(game.game_id),
        ]
    ])

    return kb


def _timeout_btn(game_id):
    return InlineKeyboardButton(text='⌛️ Timeout', callback_data=f"timeout|{game_id}"),


def _pokemon_text(player: Player):
    pokemon = player.pokemon
    shield_icon = "🛡" if pokemon.shield else ""

    return f"<b>Lvl. {pokemon.lvl} <i>{pokemon.name} {TYPES_STR[pokemon.type]} - {player.mention}</i></b>\n" \
           f"{hp_bar(pokemon.hp, pokemon.max_hp)} {shield_icon}"


def _actions_text(actions: [str]):
    if actions is None:
        return ""
    return '\n'.join(actions)


def _columns(arr, chunk_size):
    return [arr[i:i + chunk_size]
            for i in range(0, len(arr), chunk_size)]
