import random
import time
from dataclasses import dataclass
from typing import Optional

from aiogram.types import Chat, User
from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link

from bot.data.dogemons import DOGEMONS
from bot.models.pokemon import Pokemon


@dataclass
class Player:
    id: int  # telegram user id
    mention: str  # user mention

    pokemons_pool: list[str]  # names of pokemons that can be selected
    last_move_time: float  # unix time of last meaningful move (successful attack)
    pokemon: Optional[Pokemon] = None   # active pokemon

    def select_pokemon(self, pokemon_name: str):
        assert self.pokemon is None, "pokemon already selected"
        self.pokemons_pool.remove(pokemon_name)
        self.pokemon = Pokemon.new(pokemon_name)

    def attack_pokemon(self, dmg):
        self.pokemon.hp -= dmg
        if self.pokemon.hp > 0:
            return None
        pokemon = self.pokemon
        self.pokemon = None
        return pokemon

    def is_lose(self):
        return len(self.pokemons_pool) == 0

    @classmethod
    def new(cls, user: Chat | User):
        mention = markdown.hlink(user.first_name, create_tg_link("user", id=user.id))
        return cls(
            id=user.id,
            mention=mention,
            pokemons_pool=get_pokemons_pool(),
            last_move_time=time.time()
        )

    def to_mongo(self):
        return {
            "id": self.id,
            "mention": self.mention,
            "pokemon": self.pokemon.to_mongo() if self.pokemon else None,
            "pokemons_pool": self.pokemons_pool,
            "last_move_time": self.last_move_time
        }

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            id=mongo_data["id"],
            mention=mongo_data["mention"],
            pokemon=Pokemon.from_mongo(mongo_data["pokemon"]),
            pokemons_pool=mongo_data["pokemons_pool"],
            last_move_time=mongo_data["last_move_time"]
        )


def get_pokemons_pool():
    pokemons = [dogemon.name for dogemon in DOGEMONS]
    random.shuffle(pokemons)
    return pokemons[:3]
