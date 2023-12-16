import random
import time
from dataclasses import dataclass, field
from typing import Optional

from aiogram.types import Chat, User
from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link

from bot.data import const
from bot.data.const import REVIVE_HP, SLEEPING_COUNTER, REVIVE
from bot.data.dogemons import DOGEMONS
from bot.data.special_cards import SPECIAL_CARDS
from bot.models.pokemon import Pokemon


@dataclass
class Player:
    id: int  # telegram user id
    name: str  # user first name
    special_cards: [str]  # special card name

    pokemons_pool: dict  # pokemon_name => is_alive; pool of pokemons that can be selected
    last_move_time: float  # unix time of last meaningful move (successful attack)
    pokemon: Optional[Pokemon] = None  # active pokemon

    uses_of_special_cards: int = 0  # number of used special cards
    used_purchased_special_cards: [str] = field(default_factory=list)  # special cards that were purchased
    sleeping_pills_counter: [int] = None  # sleeping_pills_counter for sleeping pills
    revived_pokemon: Optional[str] = None  # pokemon name that was revived by special card

    def select_pokemon(self, pokemon_name: str):
        assert self.pokemon is None, "pokemon already selected"
        self.pokemon = Pokemon.new(pokemon_name)

        # revived pokemon will have 30% more hp
        if self.revived_pokemon == pokemon_name:
            self.pokemon.hp = self.pokemon.max_hp * REVIVE_HP

    def attack_pokemon(self, dmg):
        self.pokemon.hp -= dmg
        if self.pokemon.hp > 0:
            return None

        # pokemon dead
        pokemon = self.pokemon
        self.pokemons_pool[pokemon.name] = False  # mark pokemon as dead
        self.pokemon = None
        return pokemon

    def revive_pokemon(self, pokemon_name):
        print(self.pokemons_pool)
        self.pokemons_pool[pokemon_name] = True
        print(self.pokemons_pool)

        self.revived_pokemon = pokemon_name

    def set_sleeping_pills(self):
        self.sleeping_pills_counter = SLEEPING_COUNTER

    def decrease_sleeping_pills(self):
        self.sleeping_pills_counter -= 1
        if self.sleeping_pills_counter == 0:
            self.sleeping_pills_counter = None

    def get_pokemons_to_revive(self) -> [str]:
        return [pokemon for pokemon, is_alive in self.pokemons_pool.items() if not is_alive]

    def is_lose(self):
        return not any(is_alive for is_alive in self.pokemons_pool.values() if is_alive is True)

    def update_uses_special_cards(self):
        self.uses_of_special_cards += 1

    def update_used_purchased_special_cards(self, special_card_name):
        self.used_purchased_special_cards.append(special_card_name)

    @property
    def mention(self):
        return markdown.hlink(self.name, create_tg_link("user", id=self.id))

    @classmethod
    async def new(cls, user: Chat | User):
        return cls(
            id=user.id,
            name=user.first_name,
            pokemons_pool=get_pokemons_pool(),
            last_move_time=time.time(),
            special_cards=get_random_special(),
            sleeping_pills_counter=None,
            revived_pokemon=None,
            uses_of_special_cards=0,
            used_purchased_special_cards=[]
        )

    def to_mongo(self):
        return {
            "id": self.id,
            "name": self.name,
            "pokemon": self.pokemon.to_mongo() if self.pokemon else None,
            "pokemons_pool": self.pokemons_pool,
            "last_move_time": self.last_move_time,
            "special_cards": self.special_cards,
            "sleeping_pills_counter": self.sleeping_pills_counter if self.sleeping_pills_counter else None,
            "revived_pokemon": self.revived_pokemon if self.revived_pokemon else None,
            "uses_of_special_cards": self.uses_of_special_cards,
            "used_purchased_special_cards": self.used_purchased_special_cards
        }

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            id=mongo_data["id"],
            name=mongo_data["name"],
            pokemon=Pokemon.from_mongo(mongo_data["pokemon"]),
            pokemons_pool=mongo_data["pokemons_pool"],
            last_move_time=mongo_data["last_move_time"],
            special_cards=mongo_data["special_cards"],
            sleeping_pills_counter=mongo_data["sleeping_pills_counter"],
            revived_pokemon=mongo_data["revived_pokemon"],
            uses_of_special_cards=mongo_data["uses_of_special_cards"],
            used_purchased_special_cards=mongo_data["used_purchased_special_cards"]
        )

    def use_poison(self):
        heal_amount = self.pokemon.max_hp * const.POTION_REGEN
        new_hp = self.pokemon.hp + heal_amount
        self.pokemon.hp += heal_amount
        if new_hp > self.pokemon.max_hp:
            self.pokemon.hp = self.pokemon.max_hp
        return heal_amount


def get_pokemons_pool():
    pokemons = [dogemon.name for dogemon in DOGEMONS]
    random.shuffle(pokemons)
    return {dogemon: True for dogemon in pokemons[:3]}  # 3 random pokemons, True means that pokemon is alive


def get_random_special():
    special_cards = SPECIAL_CARDS
    random.shuffle(special_cards)
    return [REVIVE]
    return [special_cards[0]]
