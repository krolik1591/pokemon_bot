import math
import random
import time
from dataclasses import dataclass
from typing import Optional

from bot.data import const
from bot.data.const import IS_DONATE_SPECIAL, REVIVE
from bot.models.player import Player
from bot.models.pokemon_types import WEAKNESS
from bot.models.spell import Spell
from bot.utils.db_service import DbService


@dataclass
class Game:
    player1: Player
    player2: Player
    bet: int
    chat_id: int

    msg_id: Optional[int] = None

    db_service: DbService = DbService()

    game_id: Optional[str] = None
    is_player1_move: bool = True

    creation_time: float = time.time()
    winner: Optional[int] = None

    def set_msg_id(self, msg_id):
        self.msg_id = msg_id

    def select_pokemon(self, pokemon_name):
        self.get_attacker().select_pokemon(pokemon_name)

    async def revive_pokemon(self, pokemon_name):
        attacker, defender = self.get_attacker_defencer()

        if pokemon_name.endswith(IS_DONATE_SPECIAL):
            pokemon_name = pokemon_name.removesuffix(IS_DONATE_SPECIAL)

            available_donate_cards = await self.db_service.get_purchased_cards(attacker.id)
            if REVIVE not in available_donate_cards:
                raise Exception("Don't have this special card")

            attacker.update_used_purchased_special_cards(REVIVE)
            await self.db_service.subtract_special_card(attacker.id, REVIVE)
        else:
            attacker.special_cards.remove(REVIVE)

        actions = []

        if pokemon_name in attacker.get_pokemons_to_revive():
            attacker.revive_pokemon(pokemon_name)
            actions.append(f"{attacker.mention} revived {pokemon_name}")

        attacker.uses_of_special_cards += 1
        return actions

    async def use_special_card(self, special_card: str):
        attacker, defender = self.get_attacker_defencer()

        if special_card.endswith(IS_DONATE_SPECIAL):
            special_card = special_card.removesuffix(IS_DONATE_SPECIAL)

            available_donate_cards = await self.db_service.get_purchased_cards(attacker.id)
            if special_card not in available_donate_cards:
                raise Exception("Don't have this special card")

            attacker.update_used_purchased_special_cards(special_card)
            await self.db_service.subtract_special_card(attacker.id, special_card)
        else:
            attacker.special_cards.remove(special_card)

        actions = []

        if special_card == const.POTION:
            heal_amount = attacker.use_poison()
            actions.append(f"{attacker.mention} use potion and restored {math.floor(heal_amount)} hp")

        elif special_card == const.SLEEPING_PILLS:
            defender.set_sleeping_pills()
            actions.append(f"{attacker.mention} use sleeping pills! "
                           f"{defender.mention} next {const.SLEEPING_COUNTER} attack(s) will be cancelled")

        else:
            raise Exception("Unknown special card")

        attacker.uses_of_special_cards += 1

        return actions

    # returns list of actions
    def cast_spell(self, spell_name: str) -> [str]:
        attacker, defencer = self.get_attacker_defencer()
        spell = attacker.pokemon.get_spell_by_name(spell_name)

        actions = []

        # "use" spell. crash if no spells left
        spell.decrease_count()

        # just set shield if spell is defence
        if spell.is_defence:
            attacker.pokemon.set_shield()
            actions.append(f"{attacker.mention} casted shield")
            return actions

        # if has sleeping pills effect - cancel attack
        if attacker.sleeping_pills_counter is not None:
            attacker.decrease_sleeping_pills()
            actions.append(f"{attacker.mention} attack is cancelled by sleeping pills. {attacker.sleeping_pills_counter or 0} turns left")
            return actions

        # calculate dmg based on spell and pokemons types
        dmg = _calc_dmg(spell, attacker, defencer)

        # check if defencer has shield and try to attack
        if defencer.pokemon.shield:
            is_attack_canceled = defencer.pokemon.attack_shield()
            if is_attack_canceled:
                actions.append(f"{attacker.mention} attack was canceled by shield. Protected {dmg} dmg")
                return actions
            actions.append(f"{defencer.mention} shield was broken")

        # do dmg and check if pokemon dead after it
        is_pokemon_dead = defencer.attack_pokemon(dmg)
        actions.append(f"{attacker.mention} dealt {dmg} dmg by {spell.name}")
        if is_pokemon_dead:
            actions.append(f"{is_pokemon_dead.name} dead :(")

        return actions

    def end_move(self):
        self.is_player1_move = not self.is_player1_move
        self.update_last_move_time()  # start his move, reset move time

    def update_last_move_time(self):
        self.get_attacker().last_move_time = time.time()

    def is_game_over(self):
        # return (winner, loser) or None
        if self.player1.is_lose():
            return self.player2, self.player1
        if self.player2.is_lose():
            return self.player1, self.player2

    def game_over_coz_flee(self, looser_id):
        # return (winner, loser)
        if looser_id == self.player1.id:
            return self.player2, self.player1
        return self.player1, self.player2

    def is_game_over_coz_timeout(self):
        # return winner or None
        attacker, defencer = self.get_attacker_defencer()
        delta_time = time.time() - attacker.last_move_time
        if delta_time > const.TIMEOUT:
            return defencer, attacker
        return None, None

    def get_attacker_defencer(self):
        if self.get_attacker_index() == 1:
            return self.player1, self.player2
        return self.player2, self.player1

    def get_attacker_index(self) -> 1 | 2:
        return 1 if self.is_player1_move else 2

    def get_attacker(self) -> Optional[Player]:
        return self.player1 if self.is_player1_move else self.player2

    def is_player_attacks_now(self, player_id: int):
        who_must_move = self.player1.id if self.is_player1_move else self.player2.id
        return player_id == who_must_move

    def is_all_pokemons_selected(self) -> bool:
        return bool(self.player1.pokemon and self.player2.pokemon)

    @classmethod
    def new(cls, player1: Player, player2: Player, bet: Optional[int], chat_id: int):
        return cls(
            player1=player1,
            player2=player2,
            bet=bet,
            is_player1_move=random.choice((True, False)),
            winner=None,
            creation_time=time.time(),
            chat_id=chat_id,
            db_service=cls.db_service,
            msg_id=None,
        )

    @classmethod
    def from_mongo(cls, mongo_data):
        return cls(
            game_id=mongo_data['_id'],
            player1=Player.from_mongo(mongo_data['player1']),
            player2=Player.from_mongo(mongo_data['player2']),
            is_player1_move=mongo_data['is_player1_move'],
            winner=mongo_data['winner'],
            creation_time=mongo_data['creation_time'],
            bet=mongo_data['bet'],
            chat_id=mongo_data['chat_id'],
            msg_id=mongo_data['msg_id'],
        )

    def to_mongo(self):
        return {
            "player1": self.player1.to_mongo(),
            "player2": self.player2.to_mongo(),
            "is_player1_move": self.is_player1_move,
            "winner": self.winner,
            "creation_time": self.creation_time,
            "bet": self.bet,
            "chat_id": self.chat_id,
            "msg_id": self.msg_id,
        }


def _calc_dmg(spell: Spell, attack: Player, defence: Player):
    dmg = spell.attack

    if attack.pokemon.increase_dmg_by_card:
        dmg += const.ADDITION_DMG_BY_CARD

    if attack.pokemon.type in WEAKNESS[defence.pokemon.type]:
        dmg += random.randint(*const.ADDITION_DMG_BY_POKEMON_TYPE)

    return dmg
