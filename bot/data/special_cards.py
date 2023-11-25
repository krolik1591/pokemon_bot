from bot.data.const import POISON, REVIVE, SLEEPING_PILLS
from bot.models.pokemon_types import PokemonType

SPECIAL_CARDS = [REVIVE, POISON, SLEEPING_PILLS]

for pokemon_type in PokemonType:
    SPECIAL_CARDS.append(pokemon_type.value)

