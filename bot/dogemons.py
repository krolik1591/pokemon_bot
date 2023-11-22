from bot.models.pokemon_types import Types
from bot.models.spell import Spell

DOGEMON_1 = {
    'name': 'Sanya',
    'base_attack': 50,
    'hp': 150,
    'lvl': 10,
    'type': Types.WATER,
    'spells': [
        Spell('Banka', 15, False, 100),
        Spell('Pizda', 100, False, 0),
        Spell('SuperPrikol', 30, False, 5),
        Spell('RJOMBA', 50, False, 1),
    ]
}

DOGEMON_2 = {
    'name': 'Malooy',
    'base_attack': 50,
    'hp': 100,
    'lvl': 10,
    'type': Types.WATER,
    'spells': [
        Spell('Coding', 15, False, 100),
        Spell('BreakingBack', 100, False, 100),
        Spell('BreakingJunior', 30, False, 5),
        Spell('Im go high', 50, False, 1),
    ]
}

DOGEMON_3 = {
    'name': 'zaii',
    'base_attack': 50,
    'hp': 200,
    'lvl': 13,
    'type': Types.ROCK,
    'spells': [
        Spell('Tackle', 15, False, 100),
        Spell('Blaze', 100, False, 100),
        Spell('Shield', 0, True, 5),
        Spell('Skratch', 50, False, 1),
    ]
}

DOGEMON_4 = {
    'name': 'Sneaky Peek',
    'base_attack': 50,
    'hp': 120,
    'lvl': 20,
    'type': Types.ROCK,
    'spells': [
        Spell('Fireball', 15, False, 100),
        Spell('SneakyPuf', 20, False, 100),
        Spell('SneakyShield', 0, True, 5),
        Spell('ALLAHAKBAR', 100, False, 1),
    ]
}

DOGEMON_5 = {
    'name': 'Pichu',
    'base_attack': 50,
    'hp': 70,
    'lvl': 2,
    'type': Types.FIRE,
    'spells': [
        Spell('Punch', 15, False, 100),
        Spell('WaterGun', 20, False, 100),
        Spell('Bubble', 30, False, 5),
        Spell('Growl', 50, False, 1),
    ]
}

DOGEMONS = [DOGEMON_1, DOGEMON_2, DOGEMON_3, DOGEMON_4, DOGEMON_5]
DOGEMONS_MAP = {
    pokemon["name"]: pokemon
    for pokemon in DOGEMONS
}
