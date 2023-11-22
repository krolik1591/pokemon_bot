from enum import Enum


class PokemonType(Enum):
    NORMAL = 'normal'
    FIRE = 'fire'
    WATER = 'water'
    GRASS = 'grass'
    ELECTRIC = 'electric'
    ICE = 'ice'
    FIGHTING = 'fighting'
    POISON = 'poison'
    GROUND = 'ground'
    FLYING = 'flying'
    PSYCHIC = 'psychic'
    BUG = 'bug'
    ROCK = 'rock'
    GHOST = 'ghost'
    DRAGON = 'dragon'
    DARK = 'dark'
    STEEL = 'steel'
    FAIRY = 'fairy'


TYPES_STR = {
    PokemonType.NORMAL: '🌑',
    PokemonType.FIRE: '🔥',
    PokemonType.WATER: '💧',
    PokemonType.GRASS: '🌿',
    PokemonType.ELECTRIC: '⚡️',
    PokemonType.ICE: '❄️',
    PokemonType.FIGHTING: '🥊',
    PokemonType.POISON: '☠️',
    PokemonType.GROUND: '🌍',
    PokemonType.FLYING: '🦅',
    PokemonType.PSYCHIC: '🧠',
    PokemonType.BUG: '🐛',
    PokemonType.ROCK: '🪨',
    PokemonType.GHOST: '👻',
    PokemonType.DRAGON: '🐉',
    PokemonType.DARK: '🌑',
    PokemonType.STEEL: '🔩',
    PokemonType.FAIRY: '🧚',
}

WEAKNESS = {
    PokemonType.NORMAL: [PokemonType.FIGHTING],
    PokemonType.FIRE: [PokemonType.WATER, PokemonType.ROCK, PokemonType.GROUND],
    PokemonType.WATER: [PokemonType.GRASS, PokemonType.ELECTRIC],
    PokemonType.GRASS: [PokemonType.FIRE, PokemonType.ICE, PokemonType.POISON, PokemonType.FLYING, PokemonType.BUG],
    PokemonType.ELECTRIC: [PokemonType.GROUND],
    PokemonType.ICE: [PokemonType.FIRE, PokemonType.FIGHTING, PokemonType.ROCK, PokemonType.STEEL],
    PokemonType.FIGHTING: [PokemonType.FLYING, PokemonType.PSYCHIC, PokemonType.FAIRY],
    PokemonType.POISON: [PokemonType.GROUND, PokemonType.PSYCHIC],
    PokemonType.GROUND: [PokemonType.WATER, PokemonType.GRASS, PokemonType.ICE],
    PokemonType.FLYING: [PokemonType.ELECTRIC, PokemonType.ICE, PokemonType.ROCK],
    PokemonType.PSYCHIC: [PokemonType.BUG, PokemonType.GHOST, PokemonType.DARK],
    PokemonType.BUG: [PokemonType.FLYING, PokemonType.ROCK, PokemonType.FIRE],
    PokemonType.ROCK: [PokemonType.WATER, PokemonType.GRASS, PokemonType.FIGHTING, PokemonType.GROUND, PokemonType.STEEL],
    PokemonType.GHOST: [PokemonType.GHOST, PokemonType.DARK],
    PokemonType.DRAGON: [PokemonType.ICE, PokemonType.DRAGON, PokemonType.FAIRY],
    PokemonType.DARK: [PokemonType.FIGHTING, PokemonType.BUG, PokemonType.FAIRY],
    PokemonType.STEEL: [PokemonType.FIRE, PokemonType.FIGHTING, PokemonType.GROUND],
    PokemonType.FAIRY: [PokemonType.POISON, PokemonType.STEEL],
}
