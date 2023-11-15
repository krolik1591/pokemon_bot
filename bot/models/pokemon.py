from dataclasses import dataclass

from bot.dogemons import DOGEMONS, DOGEMONS_MAP


@dataclass
class Pokemon:
    name: str
    hp: int
    max_hp: int
    mp: int
    max_mp: int
    lvl: int
    type: str

    @classmethod
    def new(cls, pokemon_name):
        base_pokemon = DOGEMONS_MAP[pokemon_name]
        return cls(
            name=base_pokemon["name"],
            max_hp=base_pokemon["hp"],
            hp=base_pokemon["hp"],
            max_mp=base_pokemon["mp"],
            mp=base_pokemon["mp"],
            lvl=base_pokemon["lvl"],
            type=base_pokemon["type"]
        )

    def to_mongo(self):
        return {
            "name": self.name,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mp': self.mp,
            'max_mp': self.max_mp,
            'lvl': self.lvl,
            'type': self.type
        }
