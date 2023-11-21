import random
from dataclasses import dataclass
from typing import Optional

from aiogram.types import Chat, User

from bot.models.errors import PokemonDead
from bot.models.player import Player
from bot.models.pokemon import Pokemon


@dataclass
class Game:
    player1: Player
    player2: Player

    game_id: Optional[str] = None
    pokemon1: Optional[Pokemon] = None
    pokemon2: Optional[Pokemon] = None

    is_player1_move: bool = True

    def base_atk(self):
        who_attack, who_defence = self.pokemons_info()
        who_defence.hp -= who_attack.base_attack

    def pokemons_info(self):
        who_attack = self.pokemon1 if self.who_move_index() == 1 else self.pokemon2
        who_defense = self.pokemon2 if self.who_move_index() == 1 else self.pokemon1
        return who_attack, who_defense

    def power_atk(self):
        who_attack, who_defence = self.pokemons_info()
        who_defence.hp -= who_attack.base_attack + random.randint(3, 8)

    def special_atk(self):
        pass

    def capture(self):
        pass

    def flee(self):
        pass

    def select_pokemon(self, player_id: int, pokemon_name):
        if self.who_move_index() == 1:
            self.player1.pokemons_pool.remove(pokemon_name)
            self.pokemon1 = Pokemon.new(pokemon_name)
        else:
            self.pokemon2 = Pokemon.new(pokemon_name)
            self.player2.pokemons_pool.remove(pokemon_name)

    def end_move(self):
        self.is_player1_move = not self.is_player1_move

    def check_if_pokemon_alive(self):
        _, pokemon = self.who_move_tg_id_pokemon()
        if pokemon.hp > 0:
            return True

        if self.who_move_index() == 1:
            self.pokemon1 = None
        else:
            self.pokemon2 = None
        return False

    def have_alive_pokemons(self):
        player, _ = self.who_move_tg_id_pokemon()
        return len(player.pokemons_pool) > 0

    def get_winner_loser(self):
        loser_index = self.who_move_index()
        if loser_index == 1:
            return self.player2, self.player1
        return self.player1, self.player2


    def is_player_move(self, player_id: int):
        who_must_move = self.player1.id if self.is_player1_move else self.player2.id
        return player_id == who_must_move

    def ensure_player_move(self, player_id: int):
        assert self.is_player_move(player_id), "not ur move"

    def who_move_index(self):
        return 1 if self.is_player1_move else 2

    # todo rename to who_move_player_pokemon
    def who_move_tg_id_pokemon(self):
        return (self.player1, self.pokemon1) if self.is_player1_move else (self.player2, self.pokemon2)

    # todo rename to is_all_pokemons_selected
    def all_pokemons_selected(self):
        return self.pokemon1 and self.pokemon2

    # serialization

    @classmethod
    def new(cls, player1: Player, player2: Player):
        return cls(
            player1=player1,
            player2=player2,
        )

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            game_id=mongo_data['_id'],
            player1=Player.from_mongo(mongo_data['player1']),
            player2=Player.from_mongo(mongo_data['player2']),
            pokemon1=Pokemon.from_mongo(mongo_data['pokemon1']),
            pokemon2=Pokemon.from_mongo(mongo_data['pokemon2']),
            is_player1_move=mongo_data['is_player1_move']
        )

    def to_mongo(self):
        return {
            "player1": self.player1.to_mongo(),
            "player2": self.player2.to_mongo(),
            "pokemon1": self.pokemon1.to_mongo() if self.pokemon1 else None,
            "pokemon2": self.pokemon2.to_mongo() if self.pokemon2 else None,
            "is_player1_move": self.is_player1_move
        }
