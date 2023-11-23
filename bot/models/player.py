import random
import time
from dataclasses import dataclass
from typing import Optional

from aiogram.types import Chat, User
from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link

from bot.data.dogemons import DOGEMONS
from bot.data.special_cards import SPECIAL_CARDS
from bot.models.pokemon import Pokemon


@dataclass
class Player:
    id: int  # telegram user id
    mention: str  # user mention

    pokemons_pool: dict  # pokemon_name => is_alive; pool of pokemons that can be selected
    last_move_time: float  # unix time of last meaningful move (successful attack)
    pokemon: Optional[Pokemon] = None   # active pokemon

    special_card: Optional[str] = None  # special card name

    def select_pokemon(self, pokemon_name: str):
        assert self.pokemon is None, "pokemon already selected"
        self.pokemons_pool[pokemon_name] = False  # mark pokemon as dead
        self.pokemon = Pokemon.new(pokemon_name)

    def attack_pokemon(self, dmg):
        self.pokemon.hp -= dmg
        if self.pokemon.hp > 0:
            return None
        pokemon = self.pokemon
        self.pokemon = None
        return pokemon

    def get_pokemons_to_revive(self) -> [str]:
        return [pokemon for pokemon, is_alive in self.pokemons_pool.items() if not is_alive]

    def is_lose(self):
        return not any(is_alive for is_alive in self.pokemons_pool.values() if is_alive is True)

    @classmethod
    def new(cls, user: Chat | User):
        mention = markdown.hlink(user.first_name, create_tg_link("user", id=user.id))
        return cls(
            id=user.id,
            mention=mention,
            pokemons_pool=get_pokemons_pool(),
            last_move_time=time.time(),
            special_card=get_special_card()
        )

    def to_mongo(self):
        return {
            "id": self.id,
            "mention": self.mention,
            "pokemon": self.pokemon.to_mongo() if self.pokemon else None,
            "pokemons_pool": self.pokemons_pool,
            "last_move_time": self.last_move_time,
            "special_card": self.special_card
        }

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            id=mongo_data["id"],
            mention=mongo_data["mention"],
            pokemon=Pokemon.from_mongo(mongo_data["pokemon"]),
            pokemons_pool=mongo_data["pokemons_pool"],
            last_move_time=mongo_data["last_move_time"],
            special_card=mongo_data["special_card"]
        )


def get_pokemons_pool():
    pokemons = [dogemon.name for dogemon in DOGEMONS]
    random.shuffle(pokemons)
    return {dogemon: True for dogemon in pokemons[:3]}  # 3 random pokemons, True means that pokemon is alive


def get_special_card():
    special_cards = SPECIAL_CARDS
    random.shuffle(special_cards)
    return special_cards[0]
