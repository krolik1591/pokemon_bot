import random
from dataclasses import dataclass
from typing import Optional

from aiogram.types import Chat, User
from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link

from bot.dogemons import DOGEMONS
from bot.models.pokemon import Pokemon


@dataclass
class Player:
    id: int
    mention: str
    pokemons_pool: list[str]
    # pokemon: Optional[Pokemon] = None

    @classmethod
    def new(cls, user: Chat | User):
        mention = markdown.hlink(user.first_name, create_tg_link("user", id=user.id))
        return cls(
            id=user.id,
            mention=mention,
            pokemons_pool=get_pokemons_pool()
        )

    def to_mongo(self):
        return {
            "id": self.id,
            "mention": self.mention,
            "pokemons_pool": self.pokemons_pool
        }

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            id=mongo_data["id"],
            mention=mongo_data["mention"],
            pokemons_pool=mongo_data["pokemons_pool"]
        )


def get_pokemons_pool():
    pokemons = [dogemon['name'] for dogemon in DOGEMONS]
    random.shuffle(pokemons)
    return pokemons[:3]
