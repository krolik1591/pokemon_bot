from dataclasses import dataclass

from bot.dogemons import DOGEMONS, DOGEMONS_MAP


@dataclass
class Pokemon:
    name: str
    base_attack: int
    hp: int
    max_hp: int
    lvl: int
    type: str

    @classmethod
    def new(cls, pokemon_name):
        base_pokemon = DOGEMONS_MAP[pokemon_name]
        return cls(
            name=base_pokemon["name"],
            base_attack=base_pokemon["base_attack"],
            max_hp=base_pokemon["hp"],
            hp=base_pokemon["hp"],
            lvl=base_pokemon["lvl"],
            type=base_pokemon["type"]
        )

    @classmethod
    def from_mongo(cls, mongo_data):
        if not mongo_data:
            return None

        return cls(
            name=mongo_data["name"],
            base_attack=mongo_data["base_attack"],
            hp=mongo_data["hp"],
            max_hp=mongo_data["max_hp"],
            lvl=mongo_data["lvl"],
            type=mongo_data["type"]
        )

    def to_mongo(self):
        return {
            'name': self.name,
            'base_attack': self.base_attack,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'lvl': self.lvl,
            'type': self.type
        }
