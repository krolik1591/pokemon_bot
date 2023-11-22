import random
import time
from dataclasses import dataclass
from typing import Optional

from bot.const import TIMEOUT
from bot.models.player import Player
from bot.models.pokemon_types import WEAKNESS
from bot.models.spell import Spell


@dataclass
class Game:
    player1: Player
    player2: Player

    game_id: Optional[str] = None

    is_player1_move: bool = True


    def select_pokemon(self, pokemon_name):
        self.who_move_player().select_pokemon(pokemon_name)

    # returns list of actions
    def cast_spell(self, spell_name: str) -> [str]:
        attack, defence = self.get_attack_defence()
        spell_info: Spell = next(spell for spell in attack.pokemon.spells if spell.name == spell_name)

        if spell_info.count <= 0:
            raise Exception("No more spells")

        spell_info.count -= 1

        actions = []

        if spell_info.is_defence:
            defence.pokemon.shield = True
            actions.append(f"{attack.mention} casted shield")
            return actions

        # todo extract code below to separate func

        dmg = spell_info.attack

        if attack.pokemon.type in WEAKNESS[defence.pokemon.type]:
            dmg += random.randint(3, 8)
        if defence.pokemon.type in WEAKNESS[attack.pokemon.type]:
            dmg -= random.randint(3, 8)

        # attacker has 50% chance to miss when defender has shield
        if defence.pokemon.shield:
            defence.pokemon.shield = False
            if random.randint(0, 1) == 0:
                actions.append(f"{attack.mention} attack was canceled by defence spell. Protected {dmg} dmg")
                return actions  # return coz attack was canceled
            else:
                actions.append(f"{attack.mention} shield was broken :(")

        defence.pokemon.hp -= dmg
        actions.append(f"{attack.mention} dealt {dmg} dmg by {spell_info.name}")

        is_pokemon_dead = defence.check_pokemons()
        if is_pokemon_dead:
            actions.append(f"{is_pokemon_dead.name} dead :(")

        return actions

    def end_move(self):
        self.is_player1_move = not self.is_player1_move
        self.update_last_move_time()  # start his move, reset move time

    def update_last_move_time(self):
        self.who_move_player().last_move_time = time.time()

    def is_game_over(self):
        # return (winner, loser) or None
        if self.player1.is_lose():
            return self.player2, self.player1
        if self.player2.is_lose():
            return self.player1, self.player2


    def get_winner_if_time_out(self):
        # return winner or None
        attacker, defencer = self.get_attack_defence()
        delta_time = time.time() - attacker.last_move_time
        if delta_time > TIMEOUT:
            return defencer
        return None

    def get_attack_defence(self):
        if self.who_move_index() == 1:
            return self.player1, self.player2
        return self.player2, self.player1

    def who_move_index(self) -> 1 | 2:
        return 1 if self.is_player1_move else 2

    def who_move_player(self) -> Optional[Player]:
        return self.player1 if self.is_player1_move else self.player2

    def is_player_move(self, player_id: int):
        who_must_move = self.player1.id if self.is_player1_move else self.player2.id
        return player_id == who_must_move

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
