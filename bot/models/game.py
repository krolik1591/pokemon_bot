import random
import time
from dataclasses import dataclass
from typing import Optional

from bot.data import const
from bot.models.player import Player
from bot.models.pokemon_types import PokemonType, WEAKNESS
from bot.models.spell import Spell


@dataclass
class Game:
    player1: Player
    player2: Player
    game_id: Optional[str] = None
    is_player1_move: bool = True

    def select_pokemon(self, pokemon_name):
        self.get_attacker().select_pokemon(pokemon_name)

    def use_special_card(self, pokemon_name=None):
        POKEMON_TYPES = [_type.value for _type in PokemonType.__members__.values()]
        card_name = self.get_attacker().special_card
        attacker, defender = self.get_attacker_defencer()
        action = []
        if card_name == const.REVIVE:
            self.get_attacker().pokemons_pool[pokemon_name] = True
            self.get_attacker().set_revived_pokemon(pokemon_name)
            action.append(f"{self.get_attacker().mention} revived {pokemon_name}")

        elif card_name == const.POISON:
            add_hp = self.use_poison(attacker)
            action.append(f"{attacker.mention} use poison and restored {add_hp} hp")

        elif card_name == const.SLEEPING_PILLS:
            defender.set_sleeping_pills_counter()
            action.append(f"{attacker.mention} use sleeping pills! {defender.mention} next {const.SLEEPING_COUNTER} attack will be cancelled")

        elif card_name in POKEMON_TYPES:
            if attacker.pokemon.type == card_name:
                attacker.pokemon.increase_dmg_by_card = True
                action.append(f"{attacker.mention} use turbo {card_name} card! Attack will be increased by {const.ADDITION_DMG_BY_CARD} until current pokemon is alive")
            else:
                action.append(f"{attacker.mention} use turbo {card_name} card! But his pokemon is {attacker.pokemon.type} type. So nothing happens")

        else:
            raise Exception("Unknown special card")

        self.get_attacker().special_card = None
        return action

    # returns list of actions
    def cast_spell(self, spell_name: str) -> [str]:
        attacker, defencer = self.get_attacker_defencer()
        spell = attacker.pokemon.get_spell_by_name(spell_name)

        # "use" spell. crash if no spells left
        spell.decrease_count()

        actions = []

        # just set shield if spell is defence
        if spell.is_defence:
            attacker.pokemon.set_shield()
            actions.append(f"{attacker.mention} casted shield")
            return actions

        if self.get_attacker().sleeping_pills_counter is not None:
            self.get_attacker().decrease_sleeping_pills_counter()
            actions.append(f"{attacker.mention} attack is cancelled by sleeping pills. {self.get_attacker().sleeping_pills_counter or 0} turns left")
            return actions

        # calculate dmg based on spell and pokemons types
        dmg = _calc_dmg(spell, attacker, defencer)

        if defencer.pokemon.shield:
            is_attack_canceled = defencer.pokemon.attack_shield()
            if is_attack_canceled:
                actions.append(f"{attacker.mention} attack was canceled by shield. Protected {dmg} dmg")
                return actions
            actions.append(f"{defencer.mention} shield was broken")

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

    def is_game_over_coz_timeout(self):
        # return winner or None
        attacker, defencer = self.get_attacker_defencer()
        delta_time = time.time() - attacker.last_move_time
        if delta_time > const.TIMEOUT:
            return defencer
        return None

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

    @staticmethod
    def use_poison(attacker):
        additional_hp = attacker.pokemon.max_hp * const.POISON_REGEN
        new_hp = attacker.pokemon.hp + additional_hp
        attacker.pokemon.hp += additional_hp
        if new_hp > attacker.pokemon.max_hp:
            attacker.pokemon.hp = attacker.pokemon.max_hp
        return additional_hp

    @classmethod
    def new(cls, player1: Player, player2: Player):
        return cls(
            player1=player1,
            player2=player2,
            is_player1_move=random.choice((True, False))
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


def _calc_dmg(spell: Spell, attack: Player, defence: Player):
    dmg = spell.attack

    if attack.pokemon.increase_dmg_by_card:
        dmg += const.ADDITION_DMG_BY_CARD

    if attack.pokemon.type in WEAKNESS[defence.pokemon.type]:
        dmg += random.randint(*const.ADDITION_DMG_BY_POKEMON_TYPE)
    # if defence.pokemon.type in WEAKNESS[attack.pokemon.type]:
    #     dmg -= random.randint(3, 8)

    return dmg
