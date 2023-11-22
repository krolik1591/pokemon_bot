import random
from dataclasses import dataclass
from typing import Optional

from bot.models.player import Player
from bot.models.pokemon_types import WEAKNESS
from bot.models.spell import Spell


@dataclass
class Game:
    player1: Player
    player2: Player

    game_id: Optional[str] = None

    is_player1_move: bool = True

    def base_atk(self):
        who_attack, who_defence = self.get_attack_defence()
        who_defence.pokemon.hp -= who_attack.pokemon.base_attack

    def power_atk(self):
        who_attack, who_defence = self.get_attack_defence()
        who_defence.pokemon.hp -= who_attack.pokemon.base_attack + random.randint(3, 8)

    def special_atk(self):
        pass

    def capture(self):
        pass

    def flee(self):
        pass

    def select_pokemon(self, pokemon_name):
        self.who_move_player().select_pokemon(pokemon_name)

    def end_move(self):
        self.is_player1_move = not self.is_player1_move
        self.who_move_player().check_pokemons()

    def is_game_over(self):
        # return (winner, loser) or None
        if self.player1.is_lose():
            return self.player1, self.player2
        if self.player2.is_lose():
            return self.player2, self.player1

    def get_attack_defence(self):
        if self.who_move_index() == 1:
            return self.player1, self.player2
        return self.player2, self.player1

    def is_player_move(self, player_id: int):
        who_must_move = self.player1.id if self.is_player1_move else self.player2.id
        return player_id == who_must_move

    def who_move_index(self) -> 1 | 2:
        return 1 if self.is_player1_move else 2

    def who_move_player(self) -> Optional[Player]:
        return self.player1 if self.is_player1_move else self.player2

    def cast_spell(self, spell_name: str):
        attack, defence = self.get_attack_defence()
        spell_info: Spell = next(spell for spell in attack.pokemon.spells if spell.name == spell_name)

        if spell_info.count <= 0:
            raise Exception("No more spells")

        if spell_info.is_defence:
            attack.pokemon.shield = True
        else:
            random_bonus = random.randint(3, 8)
            additional_dmg = random_bonus if attack.pokemon.type in WEAKNESS[defence.pokemon.type] else -random_bonus
            dmg = spell_info.attack + additional_dmg

            defence.pokemon.hp -= dmg // 2 if defence.pokemon.shield else dmg

        spell_info.count -= 1

    def is_all_pokemons_selected(self) -> bool:
        return bool(self.player1.pokemon and self.player2.pokemon)

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
            is_player1_move=mongo_data['is_player1_move']
        )

    def to_mongo(self):
        return {
            "player1": self.player1.to_mongo(),
            "player2": self.player2.to_mongo(),
            "is_player1_move": self.is_player1_move
        }
