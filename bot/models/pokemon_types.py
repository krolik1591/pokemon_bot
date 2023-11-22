from enum import Enum


class Types(Enum):
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


TYPE_STR = {
    Types.NORMAL: '🌑',
    Types.FIRE: '🔥',
    Types.WATER: '💧',
    Types.GRASS: '🌿',
    Types.ELECTRIC: '⚡️',
    Types.ICE: '❄️',
    Types.FIGHTING: '🥊',
    Types.POISON: '☠️',
    Types.GROUND: '🌍',
    Types.FLYING: '🦅',
    Types.PSYCHIC: '🧠',
    Types.BUG: '🐛',
    Types.ROCK: '🪨',
    Types.GHOST: '👻',
    Types.DRAGON: '🐉',
    Types.DARK: '🌑',
    Types.STEEL: '🔩',
    Types.FAIRY: '🧚',
}

WEAKNESS = {
    Types.NORMAL: [Types.FIGHTING],
    Types.FIRE: [Types.WATER, Types.ROCK, Types.GROUND],
    Types.WATER: [Types.GRASS, Types.ELECTRIC],
    Types.GRASS: [Types.FIRE, Types.ICE, Types.POISON, Types.FLYING, Types.BUG],
    Types.ELECTRIC: [Types.GROUND],
    Types.ICE: [Types.FIRE, Types.FIGHTING, Types.ROCK, Types.STEEL],
    Types.FIGHTING: [Types.FLYING, Types.PSYCHIC, Types.FAIRY],
    Types.POISON: [Types.GROUND, Types.PSYCHIC],
    Types.GROUND: [Types.WATER, Types.GRASS, Types.ICE],
    Types.FLYING: [Types.ELECTRIC, Types.ICE, Types.ROCK],
    Types.PSYCHIC: [Types.BUG, Types.GHOST, Types.DARK],
    Types.BUG: [Types.FLYING, Types.ROCK, Types.FIRE],
    Types.ROCK: [Types.WATER, Types.GRASS, Types.FIGHTING, Types.GROUND, Types.STEEL],
    Types.GHOST: [Types.GHOST, Types.DARK],
    Types.DRAGON: [Types.ICE, Types.DRAGON, Types.FAIRY],
    Types.DARK: [Types.FIGHTING, Types.BUG, Types.FAIRY],
    Types.STEEL: [Types.FIRE, Types.FIGHTING, Types.GROUND],
    Types.FAIRY: [Types.POISON, Types.STEEL],
}
