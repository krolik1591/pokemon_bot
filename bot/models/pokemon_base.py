from dataclasses import dataclass

from bot.models.pokemon_types import PokemonType
from bot.models.spell import Spell


@dataclass
class PokemonBase:
    name: str
    hp: int
    lvl: int
    type: PokemonType
    spells: list[Spell]
