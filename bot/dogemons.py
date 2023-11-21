DOGEMON_1 = {
    'name': 'Sanya',
    'base_attack': 50,
    'hp': 150,
    'lvl': 10,
    'type': 'Fire'
}

DOGEMON_2 = {
    'name': 'Malooy',
    'base_attack': 50,
    'hp': 100,
    'lvl': 10,
    'type': 'Water'
}

DOGEMON_3 = {
    'name': 'zaii',
    'base_attack': 50,
    'hp': 200,
    'lvl': 13,
    'type': 'Earth'
}

DOGEMON_4 = {
    'name': 'Sneaky Peek',
    'base_attack': 50,
    'hp': 120,
    'lvl': 20,
    'type': 'Fire'
}

DOGEMON_5 = {
    'name': 'Pichu',
    'base_attack': 50,
    'hp': 70,
    'lvl': 2,
    'type': 'Fire'
}

DOGEMONS = [DOGEMON_1, DOGEMON_2, DOGEMON_3, DOGEMON_4, DOGEMON_5]
DOGEMONS_MAP = {
    pokemon["name"]: pokemon
    for pokemon in DOGEMONS
}
