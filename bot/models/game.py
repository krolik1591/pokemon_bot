import math
import random
import time
from dataclasses import dataclass
from pprint import pprint
from typing import Optional

from bot.data import const
from bot.data.const import IS_DONATE_EMOJI, REVIVE
from bot.models.player import Player
from bot.models.pokemon_types import WEAKNESS
from bot.models.spell import Spell
from bot.utils.db_service import DbService


@dataclass
class Game:
    players: list[Player]
    bet: int
    chat_id: int

    msg_id: Optional[int] = None

    db_service: DbService = DbService()

    game_id: Optional[str] = None
    who_move: int = 0   # index of player

    creation_time: float = time.time()
    winner: Optional[int] = None

    def set_msg_id(self, msg_id):
        self.msg_id = msg_id

    def select_pokemon(self, pokemon_name):
        attacker = self.get_attacker()
        # if len(self.players) == 2:
        attacker.select_pokemon(pokemon_name)
        return

        # previous_attacker = self.players[self.who_move - 1]




    async def revive_pokemon(self, pokemon_name, is_donate):
        attacker = self.players[self.who_move]

        if is_donate:
            await self.process_donate_special(attacker, pokemon_name, is_revive=True)
        else:
            attacker.special_cards.remove(REVIVE)

        actions = []
        if pokemon_name in attacker.get_pokemons_to_revive():
            attacker.revive_pokemon(pokemon_name)
            actions.append(f"{attacker.mention} revived {pokemon_name}")

        attacker.uses_of_special_cards += 1
        return actions

    async def use_sleeping_pills(self, defender_index: str, is_donate: bool):
        attacker = self.get_attacker()

        if is_donate:
            await self.process_donate_special(attacker, const.SLEEPING_PILLS, is_revive=False)
        else:
            attacker.special_cards.remove(const.SLEEPING_PILLS)

        actions = []

        defender = self.players[int(defender_index)]
        defender.set_sleeping_pills()
        actions.append(f"{attacker.mention} use sleeping pills! "
                       f"{defender.mention} next {const.SLEEPING_COUNTER} attack(s) will be cancelled")

        attacker.uses_of_special_cards += 1
        return actions

    async def use_potion(self, special_card, is_donate):
        attacker = self.get_attacker()
        if is_donate:
            await self.process_donate_special(attacker, special_card, is_revive=False)
        else:
            attacker.special_cards.remove(special_card)

        actions = []
        heal_amount = attacker.use_poison()
        actions.append(f"{attacker.mention} use potion and restored {math.floor(heal_amount)} hp")

        attacker.uses_of_special_cards += 1
        return actions

    async def process_donate_special(self, attacker, special_card, is_revive):
        if not is_revive:
            available_donate_cards = await self.db_service.get_purchased_cards(attacker.id)
            if special_card not in available_donate_cards:
                raise Exception("Don't have this special card")

            attacker.update_used_purchased_special_cards(special_card)
            await self.db_service.subtract_special_card(attacker.id, special_card)
        else:
            attacker.update_used_purchased_special_cards(REVIVE)
            await self.db_service.subtract_special_card(attacker.id, REVIVE)

    def get_player_by_id(self, player_id: int) -> Player:
        for player in self.players:
            if player.id == player_id:
                return player
        raise Exception("Player not found")

    # returns list of actions
    def cast_spell(self, spell_name: str, defender_index: str) -> [str]:
        # attacker, defencer = self.get_attacker_defencer_team()
        attacker = self.get_attacker()
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

        defender = self.players[int(defender_index)]

        # calculate dmg based on spell and pokemons types
        dmg = _calc_dmg(spell, attacker, defender)

        # check if defencer has shield and try to attack
        if defender.pokemon.shield:
            is_attack_canceled = defender.pokemon.attack_shield()
            if is_attack_canceled:
                actions.append(f"{attacker.mention} attack was canceled by shield. Protected {dmg} dmg")
                return actions
            actions.append(f"{defender.mention} shield was broken")

        # do dmg and check if pokemon dead after it
        is_pokemon_dead = defender.attack_pokemon(dmg)
        actions.append(f"{attacker.mention} dealt {dmg} dmg by {spell.name}")
        if is_pokemon_dead:
            actions.append(f"{is_pokemon_dead.name} dead :(")

        return actions

    def end_move(self):
        if self.who_move == len(self.players) - 1:
            self.who_move = 0
            self.update_last_move_time()  # start his move, reset move time
            return
        self.who_move += 1
        self.update_last_move_time()

    def update_last_move_time(self):
        self.get_attacker().last_move_time = time.time()

    def is_game_over(self):
        # return ([winner], [loser]) or None
        team1, team2 = self.get_teams()
        if self.is_team_lose(team1):
            return team2, team1
        if self.is_team_lose(team2):
            return team1, team2

    @staticmethod
    def is_team_lose(team):
        for player in team:
            if not player.is_lose():
                return False
        return True

    def get_teams(self):
        # return [team1], [team2]
        if len(self.players) == 2:
            return self.players[:1], self.players[1:]
        if len(self.players) == 4:
            return self.players[:2], self.players[2:]

    def game_over_coz_flee(self, looser_id):
        # return ([winner], [loser])
        team1, team2 = self.get_teams()
        if self.is_team_lose_coz_flee(team1, looser_id):
            return team2, team1
        if self.is_team_lose_coz_flee(team2, looser_id):
            return team1, team2

    @staticmethod
    def is_team_lose_coz_flee(team, looser_id):
        for player in team:
            if player.id == looser_id:
                return True
        return False

    def is_game_over_coz_timeout(self):
        # return winner or None
        attacker_team, defender_team = self.get_attacker_defencer_team()
        attacker = self.get_attacker()
        delta_time = time.time() - attacker.last_move_time
        if delta_time > const.TIMEOUT:
            return defender_team, attacker_team
        return None, None

    def get_attacker_defencer_team(self):
        team1, team2 = self.get_teams()

        if len(self.players) == 2:
            if self.who_move == 0:
                return team1, team2
            return team2, team1

        if len(self.players) == 4:
            if self.who_move in [0, 1]:
                return team1, team2
            return team2, team1

    def get_attacker(self) -> Optional[Player]:
        return self.players[self.who_move]

    def set_attacker(self, player_id: int):
        for i, player in enumerate(self.players):
            if player.id == player_id:
                self.who_move = i
                return
        raise Exception("Player not found")

    def is_player_attacks_now(self, player_id: int):
        return self.players[self.who_move].id == player_id

    def is_all_pokemons_selected(self) -> bool:
        return all(player.pokemon for player in self.players)

    @classmethod
    def new(cls, players: [Player], bet: Optional[int], chat_id: int):
        return cls(
            players=players,
            bet=bet,
            who_move=random.randint(0, len(players) - 1),
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
            players=[Player.from_mongo(player) for player in mongo_data['players']],
            who_move=mongo_data['who_move'],
            winner=mongo_data['winner'],
            creation_time=mongo_data['creation_time'],
            bet=mongo_data['bet'],
            chat_id=mongo_data['chat_id'],
            msg_id=mongo_data['msg_id'],
        )

    def to_mongo(self):
        return {
            "players": [player.to_mongo() for player in self.players],
            "who_move": self.who_move,
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
