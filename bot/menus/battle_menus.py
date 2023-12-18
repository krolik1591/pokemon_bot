from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.data import const
from bot.menus.utils_for_menus import _timeout_btn, _flee_btn, _actions_text
from bot.models.game import Game
from bot.models.player import Player
from bot.models.pokemon_types import TYPES_STR
from bot.utils.hp_bar import hp_bar


def battle_menu(game: Game, latest_actions=None):
    players_text = []
    for index, player in enumerate(game.players):
        if player.pokemon:
            players_text.append(_pokemon_text(player, index, is_dead=False))
        else:
            players_text.append(_pokemon_text(player, index, is_dead=True))

    players_text = '\n\n'.join(players_text)
    actions_text = _actions_text(latest_actions)

    player = game.get_attacker()

    text = f"{player.mention}, it's your turn to attack!\n\n" \
           f"{players_text}\n\n" \
           f"{actions_text}"

    now_attacks_text = player.name if not player.pokemon else f"{player.name} ({player.pokemon.name})"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Now attacks: {now_attacks_text} {game.who_move}", callback_data="nothing"),
        ],
        [
            InlineKeyboardButton(text='⚔ Attack', callback_data=f"fight_menu|attack|{game.game_id}"),
            InlineKeyboardButton(text='🎒 PokéBag', callback_data=f"fight_menu|special_cards|{game.game_id}"),
        ],
        [
            _timeout_btn(game.game_id, player.id),
            _flee_btn(game.game_id),
        ],
    ])

    return text, kb


def _pokemon_text(player: Player, index, is_dead):
    pokemon = player.pokemon
    emoji_team = const.BLUE_TEAM if index % 2 == 0 else const.RED_TEAM

    if is_dead:
        return f"<b>{emoji_team} {player.mention}</b>\nDEAD"

    link = f"<a href='{pokemon.url}'>{pokemon.name}</a>"
    shield_icon = "🛡" if pokemon.shield else ""
    sleeping_pills_icon = "💤" if player.sleeping_pills_counter is not None else ""
    power_increase_icon = "🔥" if pokemon.increase_dmg_by_card else ""

    return f"<b>{emoji_team}Lvl. {pokemon.lvl} {link} {TYPES_STR[pokemon.type]} - {player.mention}</b>\n" \
           f"{hp_bar(pokemon.hp, pokemon.max_hp)} {power_increase_icon} {shield_icon} {sleeping_pills_icon}"