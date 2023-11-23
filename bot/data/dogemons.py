from bot.models.pokemon_base import PokemonBase
from bot.models.pokemon_types import PokemonType
from bot.models.spell import Spell


DOGEMONS = [
    PokemonBase(
        name='Sanya',
        hp=150,
        lvl=10,
        type=PokemonType.WATER,
        spells=[
            Spell('Banka', 15, False, 100),
            Spell('Pizda', 100, False, 0),
            Spell('SuperPrikol', 30, False, 5),
            Spell('RJOMBA', 50, False, 1),
        ]
    ),
    PokemonBase(
        name='Malooy',
        hp=100,
        lvl=10,
        type=PokemonType.GRASS,
        spells=[
            Spell('Coding', 15, False, 100),
            Spell('BreakingBack', 100, False, 100),
            Spell('BreakingJunior', 30, False, 5),
            Spell('Im go high', 50, False, 1),
        ]
    ),
    PokemonBase(
        name='zaii',
        hp=200,
        lvl=13,
        type=PokemonType.ROCK,
        spells=[
            Spell('Tackle', 15, False, 100),
            Spell('Blaze', 100, False, 100),
            Spell('Shield', 0, True, 5),
            Spell('Skratch', 50, False, 1),
        ]
    ),
    PokemonBase(
        name='Sneaky Peek',
        hp=120,
        lvl=20,
        type=PokemonType.GRASS,
        spells=[
            Spell('Earthquake', 15, False, 100),
            Spell('SneakyPuf', 20, False, 100),
            Spell('SneakyShield', 0, True, 5),
            Spell('ALLAHAKBAR', 100, False, 1),
        ]
    ),
    PokemonBase(
        name='Pichu',
        hp=70,
        lvl=2,
        type=PokemonType.FIRE,
        spells=[
            Spell('Punch', 15, False, 100),
            Spell('WaterGun', 20, False, 100),
            Spell('Bubble', 30, False, 5),
            Spell('Growl', 50, False, 1),
        ]
    )
]


DOGEMONS_MAP: dict[str, PokemonBase] = {
    pokemon.name: pokemon
    for pokemon in DOGEMONS
}
