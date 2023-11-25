from typing import Set

from bot.models.pokemon_base import PokemonBase
from bot.models.pokemon_types import PokemonType
from bot.models.spell import Spell

DOGEMONS = [
    PokemonBase(
        name='Snorlax',
        hp=150,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Scratch', 6, False, 8),
            Spell('Growl', 3, False, 50),
            Spell('Rest', 0, True, 5),
            Spell('Slam', 10, False, 3),
        ]
    ),
    PokemonBase(
        name='Pidgey',
        hp=60,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Tackle', 6, False, 5),
            Spell('Wind', 0, True, 3),
            Spell('Growl', 3, False, 50),
            Spell('Gust', 15, False, 3),
        ]
    ),
    PokemonBase(
        name='Pidgeotto',
        hp=120,
        lvl=2,
        type=PokemonType.BASIC,
        spells=[
            Spell('Tackle', 5, False, 50),
            Spell('Gust', 20, False, 3),
            Spell('Peck', 6, False, 5),
            Spell('Wing hit', 10, False, 2),
        ]
    ),
    PokemonBase(
        name='Rattata',
        hp=50,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Scratch', 3, False, 50),
            Spell('Quick hit', 8, False, 3),
            Spell('Tackle', 5, False, 3),
            Spell('Focus', 0, True, 3),
        ]
    ),
    PokemonBase(
        name='Raticate',
        hp=90,
        lvl=2,
        type=PokemonType.BASIC,
        spells=[
            Spell('Scratch', 3, False, 50),
            Spell('Teeth hit', 8, False, 3),
            Spell('Hit', 10, False, 3),
            Spell('Tailwhip', 7, False, 1),
        ]
    ),
    PokemonBase(
        name='Jigglypuff',
        hp=50,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Rollout', 8, False, 3),
            Spell('Pound', 8, False, 3),
            Spell('Slap', 4, False, 30),
            Spell('Sing', 0, True, 5),
        ]
    ),
    PokemonBase(
        name='Meowth',
        hp=70,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Scratch', 3, False, 30),
            Spell('Fury', 8, False, 3),
            Spell('Cat kick', 9, False, 3),
            Spell('Confuse', 0, True, 5),
        ]
    ),
    PokemonBase(
        name='Doduo',
        hp=70,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Peck', 8, False, 3),
            Spell('Quick hit', 7, False, 3),
            Spell('Run', 0, True, 3),
            Spell('Stab', 5, False, 3),
        ]
    ),
    PokemonBase(
        name='Dodrio',
        hp=120,
        lvl=2,
        type=PokemonType.BASIC,
        spells=[
            Spell('top peck', 10, False, 3),
            Spell('Double hit', 7, False, 3),
            Spell('Strike', 3, False, 50),
            Spell('Tri attack', 6, False, 3),
        ]
    ),
    PokemonBase(
        name='Hoothoot',
        hp=40,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Confuse', 0, True, 5),
            Spell('Peck', 7, False, 3),
            Spell('Scratch', 3, False, 50),
            Spell('Fly hit', 5, False, 3),
        ]
    ),
    PokemonBase(
        name='Squirtle',
        hp=80,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Tackle', 5, False, 55),
            Spell('Water punch', 12, False, 3),
            Spell('splash', 6, False, 3),
            Spell('Shell hit', 5, False, 3),
        ]
    ),
    PokemonBase(
        name='Blastoise',
        hp=150,
        lvl=2,
        type=PokemonType.WATER,
        spells=[
            Spell('Tackle', 5, False, 55),
            Spell('Water gun', 15, False, 3),
            Spell('Bubble', 8, False, 3),
            Spell('Shell hit', 6, False, 3),
        ]
    ),
    PokemonBase(
        name='Staryu',
        hp=70,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Smack', 4, False, 55),
            Spell('Quick spin', 11, False, 3),
            Spell('Splash', 5, False, 6),
            Spell('Water jet', 6, False, 3),
        ]
    ),
    PokemonBase(
        name='Tentacruel',
        hp=150,
        lvl=2,
        type=PokemonType.WATER,
        spells=[
            Spell('Wrap', 10, False, 2),
            Spell('Tight Sting', 11, False, 3),
            Spell('Splash', 5, False, 60),
            Spell('Supersclosis', 15, False, 2),
        ]
    ),
    PokemonBase(
        name='Krabby',
        hp=80,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Bite', 4, False, 25),
            Spell('Swim Deep', 0, True, 3),
            Spell('Grip', 8, False, 3),
            Spell('Shower', 7, False, 4),
        ]
    ),
    PokemonBase(
        name='Horsea',
        hp=50,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Bite', 4, False, 25),
            Spell('Water throw', 3, False, 30),
            Spell('Splash', 5, False, 3),
            Spell('Shower', 7, False, 2),
        ]
    ),
    PokemonBase(
        name='Geodude',
        hp=100,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Rock throw', 9, False, 2),
            Spell('Tackle', 3, False, 30),
            Spell('Punch', 5, False, 3),
            Spell('Linear hit', 7, False, 2),
        ]
    ),
    PokemonBase(
        name='Golem',
        hp=180,
        lvl=2,
        type=PokemonType.ROCK,
        spells=[
            Spell('Stone Edge', 15, False, 2),
            Spell('Lunge', 11, False, 4),
            Spell('Tumble', 3, False, 30),
            Spell('Mega hit', 10, False, 2),
        ]
    ),
    PokemonBase(
        name='Onix',
        hp=250,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Rock Throw', 15, False, 2),
            Spell('X Impact', 15, False, 4),
            Spell('Dig', 0, True, 3),
            Spell('Harden', 3, False, 20),
        ]
    ),
    PokemonBase(
        name='Sudowoodo',
        hp=140,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Double Throw', 10, False, 2),
            Spell('Tackle', 3, False, 40),
            Spell('Dance', 0, True, 3),
            Spell('Chop', 6, False, 3),
        ]
    ),
    PokemonBase(
        name='Rhyhorn',
        hp=160,
        lvl=2,
        type=PokemonType.ROCK,
        spells=[
            Spell('Tight Hit', 10, False, 3),
            Spell('Crush', 9, False, 2),
            Spell('Horn smash', 5, False, 3),
            Spell('Chop', 3, False, 30),
        ]
    ),
    PokemonBase(
        name='Omastar',
        hp=200,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Spin Hit', 10, False, 3),
            Spell('Bind', 4, False, 50),
            Spell('Confuse', 0, True, 3),
            Spell('Time Spin', 8, False, 3),
        ]
    ),
    PokemonBase(
        name='Bulbasaur',
        hp=70,
        lvl=1,
        type=PokemonType.GRASS,
        spells=[
            Spell('Hit', 3, False, 30),
            Spell('Tackle', 5, False, 5),
            Spell('Leaf Sting', 9, False, 2),
            Spell('X seed', 0, True, 3),
        ]
    ),
    PokemonBase(
        name='Venusaur',
        hp=150,
        lvl=2,
        type=PokemonType.GRASS,
        spells=[
            Spell('Razor Leaf', 15, False, 3),
            Spell('Bite', 5, False, 50),
            Spell('Leaf Sting', 10, False, 2),
            Spell('Scrach', 3, False, 30),
        ]
    ),
    PokemonBase(
        name='Gloom',
        hp=100,
        lvl=1,
        type=PokemonType.GRASS,
        spells=[
            Spell('Razor Leaf', 9, False, 3),
            Spell('Drool', 5, False, 2),
            Spell('Sleep spell', 0, True, 3),
            Spell('Scrach', 3, False, 30),
        ]
    ),
    PokemonBase(
        name='Parasect',
        hp=150,
        lvl=2,
        type=PokemonType.GRASS,
        spells=[
            Spell('X Leaf', 5, False, 3),
            Spell('Slash', 10, False, 3),
            Spell('Claw hit', 5, False, 3),
            Spell('Scrach', 3, False, 30),
        ]
    ),
    PokemonBase(
        name='Chikorita',
        hp=60,
        lvl=1,
        type=PokemonType.GRASS,
        spells=[
            Spell('Leaf slash', 9, False, 2),
            Spell('Tackle', 4, False, 30),
            Spell('Head hit', 6, False, 3),
            Spell('Run', 0, True, 3),
        ]
    ),
    PokemonBase(
        name='Victreebel',
        hp=150,
        lvl=2,
        type=PokemonType.GRASS,
        spells=[
            Spell('Acid', 10, False, 3),
            Spell('Sting', 5, False, 3),
            Spell('Swallow', 5, False, 5),
            Spell('Leaf throw', 4, False, 30),
        ]
    ),
    PokemonBase(
        name='Charmander',
        hp=80,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Tackle', 3, False, 30),
            Spell('Scratch', 5, False, 5),
            Spell('Flare', 15, False, 2),
            Spell('Heat up', 4, False, 10),
        ]
    ),
    PokemonBase(
        name='Charizard',
        hp=180,
        lvl=2,
        type=PokemonType.FIRE,
        spells=[
            Spell('Ember X', 20, False, 1),
            Spell('Blaze', 8, False, 2),
            Spell('flames', 5, False, 30),
            Spell('Fire spin', 10, False, 2),
        ]
    ),
    PokemonBase(
        name='Vulpix',
        hp=70,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Flare', 7, False, 3),
            Spell('Confuse ray', 0, True, 3),
            Spell('Brushfire', 5, False, 5),
            Spell('Scratch', 2, False, 40),
        ]
    ),
    PokemonBase(
        name='Arcanine',
        hp=150,
        lvl=2,
        type=PokemonType.FIRE,
        spells=[
            Spell('Fire maze', 15, False, 3),
            Spell('Sun Burn', 8, False, 3),
            Spell('Flame throw', 5, False, 5),
            Spell('Scratch', 3, False, 40),
        ]
    ),
    PokemonBase(
        name='Magmar',
        hp=80,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Fire kick', 8, False, 3),
            Spell('Low kick', 5, False, 3),
            Spell('Fire jix', 5, False, 3),
            Spell('Scratch', 3, False, 40),
        ]
    ),
    PokemonBase(
        name='Cyndaquil',
        hp=90,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Tackle', 3, False, 35),
            Spell('Sleep', 0, True, 3),
            Spell('Swift', 5, False, 3),
            Spell('Fireworks', 9, False, 3),
        ]
    ),
    PokemonBase(
        name='Gastly',
        hp=60,
        lvl=1,
        type=PokemonType.GHOST,
        spells=[
            Spell('Fade out', 0, True, 3),
            Spell('Soul bound', 10, False, 3),
            Spell('Nightmare', 15, False, 3),
            Spell('Sleep poison', 15, False, 3),
        ]
    ),
    PokemonBase(
        name='Haunter',
        hp=70,
        lvl=2,
        type=PokemonType.GHOST,
        spells=[
            Spell('Sponky shot', 10, False, 3),
            Spell('Shadow ball', 10, False, 3),
            Spell('Nightmare', 15, False, 3),
            Spell('Dreameater', 15, False, 3),
        ]
    ),
    PokemonBase(
        name='Gengar',
        hp=100,
        lvl=3,
        type=PokemonType.GHOST,
        spells=[
            Spell('Pain burst', 20, False, 1),
            Spell('Curse', 8, False, 20),
            Spell('Shadow Skip', 15, False, 3),
            Spell('Soul crush', 20, False, 1),
        ]
    ),
    PokemonBase(
        name='Pikachu',
        hp=70,
        lvl=1,
        type=PokemonType.ELECTRIC,
        spells=[
            Spell('Electro ball', 20, False, 1),
            Spell('Charge', 0, True, 3),
            Spell('Tackle', 4, False, 30),
            Spell('Pike strike', 5, False, 5),
        ]
    ),
    PokemonBase(
        name='Raichu',
        hp=120,
        lvl=2,
        type=PokemonType.ELECTRIC,
        spells=[
            Spell('Electro Spark', 15, False, 3),
            Spell('Shock wave', 9, False, 3),
            Spell('Tail Spark', 7, False, 5),
            Spell('Voltage hit', 5, False, 5),
        ]
    ),
    PokemonBase(
        name='Magneton',
        hp=120,
        lvl=2,
        type=PokemonType.ELECTRIC,
        spells=[
            Spell('Electric dip', 10, False, 2),
            Spell('Shock stess', 5, False, 5),
            Spell('Quick hit', 4, False, 50),
            Spell('electro bomb', 15, False, 1),
        ]
    ),
    PokemonBase(
        name='mewtwo',
        hp=250,
        lvl=10,
        type=PokemonType.LEGENDARY,
        spells=[
            Spell('Psychic', 20, False, 2),
            Spell('Life crush', 40, False, 1),
            Spell('Meditate', 0, True, 5),
            Spell('Burst', 5, False, 50),
        ]
    ),
    PokemonBase(
        name='Moltres',
        hp=270,
        lvl=10,
        type=PokemonType.LEGENDARY,
        spells=[
            Spell('Death Flames', 30, False, 2),
            Spell('Big bang', 40, False, 1),
            Spell('Body crush', 10, True, 5),
            Spell('Fire Spin', 5, False, 50),
        ]
    ),
    PokemonBase(
        name='Zapdos',
        hp=260,
        lvl=10,
        type=PokemonType.LEGENDARY,
        spells=[
            Spell('ThunderBolt', 5, False, 25),
            Spell('Thunderstorm', 30, False, 1),
            Spell('Soul swallow', 25, True, 2),
            Spell('Infinite Volt', 30, False, 1),
        ]
    ),
]

DOGEMONS_MAP: dict[str, PokemonBase] = {
    pokemon.name: pokemon
    for pokemon in DOGEMONS
}
