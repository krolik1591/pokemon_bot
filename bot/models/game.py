from dataclasses import dataclass
from typing import Optional

from bot.models.pokemon import Pokemon


@dataclass
class Game:
    player1: int
    player2: int

    game_id: Optional[str] = None
    pokemon1: Optional[Pokemon] = None
    pokemon2: Optional[Pokemon] = None

    is_player1_move: bool = True

    def base_atk(self):
        pass

    def special_atk(self):
        pass

    def capture(self):
        pass

    def flee(self):
        pass

    def select_pokemon(self, player, pokemon_name):
        if self.which_player(player) == 1:
            self.pokemon1 = Pokemon.new(pokemon_name)
        else:
            self.pokemon2 = Pokemon.new(pokemon_name)

    def end_move(self):
        self.is_player1_move = not self.is_player1_move

    def ensure_player_move(self, player):
        assert self.who_move_tg_id() == player, "not ur move"

    def which_player(self, player):
        player_index = [self.player1, self.player2].index(player)
        assert player_index != -1, "player not found"
        return player_index + 1    # 1 or 2

    def who_move_index(self):
        return 1 if self.is_player1_move else 2

    def who_move_tg_id(self):
        return self.player1 if self.is_player1_move else self.player2

    # serialization

    @classmethod
    def new(cls, player1, player2):
        return cls(
            player1=player1,
            player2=player2,
        )

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            game_id=mongo_data['_id'],
            player1=mongo_data['player1'],
            player2=mongo_data['player2'],
            pokemon1=Pokemon.from_mongo(mongo_data['pokemon1']) if mongo_data['pokemon1'] else None,
            pokemon2=Pokemon.from_mongo(mongo_data['pokemon2']) if mongo_data['pokemon2'] else None,
            is_player1_move=mongo_data['is_player1_move']
        )

    def to_mongo(self):
        return {
            "player1": self.player1,
            "player2": self.player2,
            "pokemon1": self.pokemon1.to_mongo() if self.pokemon1 else None,
            "pokemon2": self.pokemon2.to_mongo() if self.pokemon2 else None,
            "is_player1_move": self.is_player1_move
        }
