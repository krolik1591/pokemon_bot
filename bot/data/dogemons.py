from typing import Set

from bot.models.pokemon_base import PokemonBase
from bot.models.pokemon_types import PokemonType
from bot.models.spell import Spell

DOGEMONS = [
    PokemonBase(
        name='Snorlex',
        hp=150,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Tight Slam', 9, False, 5),
            Spell('Punch', 6, False, 50),
            Spell('Rest', 0, True, 5),
            Spell('Heavt Imapct', 15, False, 1),
        ]
    ),
    PokemonBase(
        name='Pidgei',
        hp=60,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Wings cut', 9, False, 5),
            Spell('WindSpin', 0, True, 3),
            Spell('Tackle', 6, False, 50),
            Spell('Gust', 18, False, 2),
        ]
    ),
    PokemonBase(
        name='Pidgiotto',
        hp=120,
        lvl=2,
        type=PokemonType.BASIC,
        spells=[
            Spell('Tackle', 6, False, 50),
            Spell('Gust', 18, False, 3),
            Spell('Peck', 8, False, 3),
            Spell('Wing hit', 8, False, 5),
        ]
    ),
    PokemonBase(
        name='Rattatey',
        hp=50,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Scratch', 5, False, 50),
            Spell('Quick hit', 9, False, 3),
            Spell('Tackle', 8, False, 3),
            Spell('Focus', 0, True, 3),
        ]
    ),
    PokemonBase(
        name='Raticatta',
        hp=90,
        lvl=2,
        type=PokemonType.BASIC,
        spells=[
            Spell('Scratch', 6, False, 50),
            Spell('Poison Bite', 15, False, 1),
            Spell('Tail Hit', 10, False, 3),
            Spell('Tailwhip', 9, False, 3),
        ]
    ),
    PokemonBase(
        name='Jigglimuff',
        hp=50,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Rollout', 10, False, 3),
            Spell('Pound', 10, False, 3),
            Spell('Slap', 5, False, 50),
            Spell('Sing', 0, True, 5),
        ]
    ),
        PokemonBase(
        name='Miowth',
        hp=70,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Scratch', 5, False, 50),
            Spell('Scream Out', 10, False, 3),
            Spell('Cat kick', 10, False, 3),
            Spell('Confuse', 0, True, 3),
        ]
    ),
        PokemonBase(
        name='Taures',
        hp=110,
        lvl=1,
        type=PokemonType.BASIC,
        spells=[
            Spell('Combat hit', 13, False, 3),
            Spell('Horn fury', 9, False, 2),
            Spell('TakeDown', 5, False, 50),
            Spell('Rage', 8, False, 5),
        ]
    ),
        PokemonBase(
        name='Scuirtle',
        hp=80,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Tackle', 5, False, 55),
            Spell('Water punch', 16, False, 3),
            Spell('splash', 8, False, 3),
            Spell('Shell hit', 7, False, 5),
        ]
    ),
        PokemonBase(
        name='Blastoicey',
        hp=150,
        lvl=2,
        type=PokemonType.WATER,
        spells=[
            Spell('Tackle', 6, False, 55),
            Spell('Water gun', 18, False, 3),
            Spell('Bubble', 8, False, 3),
            Spell('Shell hit', 6, False, 3),
        ]
    ),
        PokemonBase(
        name='Starey',
        hp=70,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Smack', 4, False, 55),
            Spell('Quick spin', 8, False, 4),
            Spell('Splash', 7, False, 6),
            Spell('Water jet', 9, False, 3),
        ]
    ),
        PokemonBase(
        name='Tenticruel',
        hp=170,
        lvl=2,
        type=PokemonType.WATER,
        spells=[
            Spell('Wrap', 13, False, 5),
            Spell('Tight Sting', 14, False, 3),
            Spell('Splash', 5, False, 60),
            Spell('Supersclosis', 16, False, 2),
        ]
    ),
        PokemonBase(
        name='Crabby',
        hp=80,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Bite', 5, False, 25),
            Spell('Swim Deep', 0, True, 3),
            Spell('Gel Grip', 10, False, 3),
            Spell('Shower', 9, False, 4),
        ]
    ),
        PokemonBase(
        name='Seahorse',
        hp=50,
        lvl=1,
        type=PokemonType.WATER,
        spells=[
            Spell('Bite', 6, False, 25),
            Spell('Water Beam', 5, False, 30),
            Spell('Splash', 8, False, 3),
            Spell('Shower', 9, False, 2),
        ]
    ),
        PokemonBase(
        name='Giodude',
        hp=100,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Rock throw', 13, False, 2),
            Spell('Tackle', 5, False, 30),
            Spell('Punch', 9, False, 3),
            Spell('Linear hit', 9, False, 4),
        ]
    ),
        PokemonBase(
        name='Golim',
        hp=180,
        lvl=2,
        type=PokemonType.ROCK,
        spells=[
            Spell('Stone Edge', 16, False, 2),
            Spell('Lunge', 13, False, 4),
            Spell('Tumble', 6, False, 30),
            Spell('Mega hit', 14, False, 2),
        ]
    ),
        PokemonBase(
        name='Onix',
        hp=210,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Rock Shower', 16, False, 5),
            Spell('Stone Impact', 9, False, 4),
            Spell('Deep Dig', 0, True, 3),
            Spell('RockHit', 6, False, 50),
        ]
    ),
        PokemonBase(
        name='Sudowoodo',
        hp=140,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Double Throw', 10, False, 5),
            Spell('Tackle', 5, False, 40),
            Spell('Dance', 0, True, 3),
            Spell('Chop', 9, False, 3),
        ]
    ),
        PokemonBase(
        name='Rhihorn',
        hp=110,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Tight Hit', 13, False, 5),
            Spell('Crush', 10, False, 3),
            Spell('Horn smash', 5, False, 7),
            Spell('Chop', 4, False, 50),
        ]
    ),
        PokemonBase(
        name='Aerodactile',
        hp=190,
        lvl=1,
        type=PokemonType.ROCK,
        spells=[
            Spell('Spin Hit', 14, False, 3),
            Spell('Bind Attack', 6, False, 50),
            Spell('Fossil fangs', 9, False, 5),
            Spell('Wing Spin', 9, False, 3),
        ]
    ),
        PokemonBase(
        name='Bulbasor',
        hp=90,
        lvl=1,
        type=PokemonType.GRASS,
        spells=[
            Spell('Quick Hit', 5, False, 30),
            Spell('Leaf Cut', 9, False, 8),
            Spell('Green Razors', 13, False, 3),
            Spell('Sleep seed', 0, True, 3),
        ]
    ),
        PokemonBase(
        name='Venusor',
        hp=150,
        lvl=2,
        type=PokemonType.GRASS,
        spells=[
            Spell('Razor Leaf', 16, False, 4),
            Spell('Sap Bite', 9, False, 9),
            Spell('Leaf Sting', 12, False, 2),
            Spell('Sling Scrach', 6, False, 30),
        ]
    ),
        PokemonBase(
        name='scither',
        hp=100,
        lvl=1,
        type=PokemonType.GRASS,
        spells=[
            Spell('Razor Leaf', 13, False, 3),
            Spell('Drool', 9, False, 3),
            Spell('Sleep spell', 0, True, 3),
            Spell('Scrach', 7, False, 30),
        ]
    ),

        PokemonBase(
        name='Tangila',
        hp=80,
        lvl=1,
        type=PokemonType.GRASS,
        spells=[
            Spell('Vine Tease', 12, False, 5),
            Spell('Gentle Slap', 5, False, 50),
            Spell('Grass Knot',9, False, 5),
            Spell('Run', 0, True, 3),
        ]
    ),
        PokemonBase(
        name='exiggutor',
        hp=150,
        lvl=2,
        type=PokemonType.GRASS,
        spells=[
            Spell('Super Eggsplosion', 13, False, 4),
            Spell('Seed bullets', 8, False, 5),
            Spell('Stomp',12, False, 3),
            Spell('Leaf throw', 6, False, 30),
        ]
    ),
        PokemonBase(
        name='charmandar',
        hp=80,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Tackle', 6, False, 30),
            Spell('Fire balls', 9, False, 5),
            Spell('Flare',15, False, 2),
            Spell('Heat up', 6, False, 30),
        ]
    ),
        PokemonBase(
        name='Charizard',
        hp=180,
        lvl=2,
        type=PokemonType.FIRE,
        spells=[
            Spell('Ember', 7, False, 40),
            Spell('Fury Blaze', 14, False, 3),
            Spell('flames',9, False, 5),
            Spell('Fire spin', 15, False, 3),
        ]
    ),
        PokemonBase(
        name='Vulpex',
        hp=70,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Flare', 9, False, 3),
            Spell('Confuse ray', 0, True, 3),
            Spell('Tail Fire',15, False, 2),
            Spell('Scratch', 4, False, 40),
        ]
    ),
        PokemonBase(
        name='Arkanine',
        hp=150,
        lvl=2,
        type=PokemonType.FIRE,
        spells=[
            Spell('Fire maze', 15, False, 3),
            Spell('Sun Burn', 9, False, 3),
            Spell('Flame throw',8, False, 5),
            Spell('Scratch', 5, False, 40),
        ]
    ),
        PokemonBase(
        name='Magmer',
        hp=80,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Fire kick', 13, False, 3),
            Spell('Flame showers', 8, False, 5),
            Spell('Fire jix',9, False, 3),
            Spell('Scratch', 4, False, 40),
        ]
    ),
        PokemonBase(
        name='Cyndakuil',
        hp=90,
        lvl=1,
        type=PokemonType.FIRE,
        spells=[
            Spell('Tackle', 4, False, 35),
            Spell('Heat Sleep', 0, True, 3),
            Spell('Volvano clouds',13, False, 3),
            Spell('Fireworks', 11, False, 3),
        ]
    ),
        PokemonBase(
        name='Gasly',
        hp=60,
        lvl=1,
        type=PokemonType.GHOST,
        spells=[
            Spell('Fade out', 0, True, 3),
            Spell('Soul pin', 13, False, 5),
            Spell('Nightmare',15, False, 3),
            Spell('Gas Attack', 6, False, 50),
        ]
    ),
        PokemonBase(
        name='Haunter',
        hp=50,
        lvl=2,
        type=PokemonType.GHOST,
        spells=[
            Spell('Sponky shot', 7, False, 30),
            Spell('Shadow ball', 13, False, 3),
            Spell('Nightmare',16, False, 3),
            Spell('Dreameater', 16, False, 3),
        ]
    ),
        PokemonBase(
        name='Genger',
        hp=60,
        lvl=3,
        type=PokemonType.GHOST,
        spells=[
            Spell('Pain burst', 20, False, 1),
            Spell('Curse', 13, False, 20),
            Spell('Shadow Skip',17, False, 3),
            Spell('Soul crush', 25, False, 1),
        ]
    ),
        PokemonBase(
        name='Pekachu',
        hp=70,
        lvl=1,
        type=PokemonType.ELECTRIC,
        spells=[
            Spell('Electro ball', 20, False, 1),
            Spell('Charge', 0, True, 3),
            Spell('Tackle',5, False, 50),
            Spell('Pike strike', 12, False, 5),
        ]
    ),
        PokemonBase(
        name='Raechu',
        hp=120,
        lvl=2,
        type=PokemonType.ELECTRIC,
        spells=[
            Spell('Electro Spark', 17, False, 3),
            Spell('Shock wave', 12, False, 3),
            Spell('Tail Spark',9, False, 5),
            Spell('Voltage hit', 6, False, 50),
        ]
    ),
        PokemonBase(
        name='Elektrode',
        hp=60,
        lvl=1,
        type=PokemonType.ELECTRIC,
        spells=[
            Spell('Electric dip', 13, False, 1),
            Spell('Shock stess', 8, False, 5),
            Spell('Quick hit',5, False, 50),
            Spell('electro roll', 11, False, 3),
        ]
    ),
        PokemonBase(
        name='mewtu',
        hp=250,
        lvl=10,
        type=PokemonType.LEGENDARY,
        spells=[
            Spell('Psychic', 15, False, 3),
            Spell('Big Bang', 40, False, 1),
            Spell('Meditate',0, True, 5),
            Spell('Burst', 5, False, 50),
        ]
    ),
        PokemonBase(
        name='Moltras',
        hp=230,
        lvl=10,
        type=PokemonType.LEGENDARY,
        spells=[
            Spell('Death Flames', 30, False, 2),
            Spell('Soul Burn', 40, False, 1),
            Spell('Earth Crush',10, True, 2),
            Spell('Fire Spin', 5, False, 50),
        ]
    )
]

DOGEMONS_MAP: dict[str, PokemonBase] = {
    pokemon.name: pokemon
    for pokemon in DOGEMONS
}
