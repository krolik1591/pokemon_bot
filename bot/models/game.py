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

    def end_move(self):
        self.is_player1_move = not self.is_player1_move

    def ensure_player_move(self, player):
        who_must_move = self.player1 if self.is_player1_move else self.player2
        assert player == who_must_move, "not ur move"

    # serialization

    @classmethod
    def new(cls, player1, player2):
        return cls(
            player1=player1,
            player2=player2,
        )

    def select_pokemon(self, player, pokemon_name):
        if self.which_player(player) == 1:
            self.pokemon1 = Pokemon.new(pokemon_name)
        else:
            self.pokemon2 = Pokemon.new(pokemon_name)

    def which_player(self, player):
        index_player = [self.player1, self.player2].index(player)
        assert index_player != -1, "player not found"
        return index_player + 1    # 1 or 2

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            game_id=mongo_data.id,
            player1=mongo_data.player1,
        )

    def to_mongo(self):
        return {
            "game_id": self.game_id,
            "player1": self.player1,
            "player2": self.player2,
            "pokemon1": self.pokemon1.to_mongo(),
            "pokemon2": self.pokemon2.to_mongo(),
            "is_player1_move": self.is_player1_move
        }
