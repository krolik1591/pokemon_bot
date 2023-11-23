import random
from dataclasses import dataclass

from bot.data.dogemons import DOGEMONS_MAP
from bot.models.pokemon_base import PokemonBase
from bot.models.spell import Spell


@dataclass
class Pokemon:
    base_pokemon: PokemonBase
    spells: [Spell]
    hp: int
    shield: bool = False
    increase_dmg_by_card: bool = False  # increase_dmg_by_card for special card

    @property
    def name(self):
        return self.base_pokemon.name

    @property
    def max_hp(self):
        return self.base_pokemon.hp

    @property
    def lvl(self):
        return self.base_pokemon.lvl

    @property
    def type(self):
        return self.base_pokemon.type

    def set_shield(self):
        if self.shield:
            raise Exception("Already have shield")
        self.shield = True

    def attack_shield(self) -> str:
        assert self.shield, "No shield"
        self.shield = False
        return random.choice((True, False))  # is attack cancelled

    def get_spell_by_name(self, spell_name: str) -> Spell:
        return next(spell for spell in self.spells if spell.name == spell_name)

    @classmethod
    def new(cls, pokemon_name):
        base_pokemon = DOGEMONS_MAP[pokemon_name]
        return cls(
            base_pokemon=base_pokemon,
            hp=base_pokemon.hp,
            spells=_spells_from_remaining_count(base_pokemon)
        )

    @classmethod
    def from_mongo(cls, mongo_data):
        if not mongo_data:
            return None

        base_pokemon = DOGEMONS_MAP[mongo_data["name"]]
        return cls(
            base_pokemon=base_pokemon,
            hp=mongo_data["hp"],
            spells=_spells_from_remaining_count(base_pokemon, mongo_data["spells_remaining_count"]),
            shield=mongo_data["shield"],
            increase_dmg_by_card=mongo_data["increase_dmg_by_card"]
        )

    def to_mongo(self):
        return {
            'name': self.name,
            'hp': self.hp,
            'spells_remaining_count': _spells_to_remaining_count(self.spells),
            "shield": self.shield,
            "increase_dmg_by_card": self.increase_dmg_by_card
        }


def _spells_from_remaining_count(base_pokemon: PokemonBase, remaining_count: [int] = None) -> [Spell]:
    return [
        spell.with_count(remaining_count[i] if remaining_count else None)
        for i, spell in enumerate(base_pokemon.spells)
    ]


def _spells_to_remaining_count(spells: [Spell]) -> [int]:
    return [i.count for i in spells]
