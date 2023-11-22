from enum import Enum


class Types(Enum):
    FIRE = 'fire'
    WATER = 'water'
    EARTH = 'earth'
    AIR = 'air'
    ROCK = 'rock'
    NORMAL = 'normal'


TYPE_STR = {
    Types.FIRE: '🔥',
    Types.WATER: '💧',
    Types.EARTH: '🌿',
    Types.AIR: '💨',
    Types.ROCK: '🗿',
    Types.NORMAL: '🐱',
}
