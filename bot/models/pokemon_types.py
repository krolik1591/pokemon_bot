from enum import Enum


class Types(Enum):
    NORMAL = 'normal'
    FIRE = 'fire'
    WATER = 'water'
    GRASS = 'grass'
    ELECTRIC = 'electric'
    ICE = 'ice'
    FIGHTING = 'fighting'


TYPE_STR = {
    Types.NORMAL: '🌑',
    Types.FIRE: '🔥',
    Types.WATER: '💧',
    Types.GRASS: '🌿',
    Types.ELECTRIC: '⚡️',
    Types.ICE: '❄️',
    Types.FIGHTING: '🥊',
}
