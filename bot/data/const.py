TIMEOUT = 5  # seconds

SLEEPING_COUNTER = 3  # how many moves pokemon will sleep
POTION_REGEN = 0.5   # MAX_HP * POTION_REGEN
ADDITION_DMG_BY_CARD = 5  # how many dmg will increase by card
REVIVE_HP = 0.3  # MAX_HP * REVIVE_HP

MAX_USES_OF_SPECIAL_CARDS = 3  # how many times player can use special cards

ADDITION_DMG_BY_POKEMON_TYPE = (3, 8)  # how many dmg will increase by pokemon type

MAX_ACTIVE_GAMES = 2

REWARD = 0.95
PRIZE_POOL = 0.05

# name special cards
# TURBO_BONUS card name is in bot/data/special_cards.py
POTION = "Potion"
SLEEPING_PILLS = "Sleeping pills"
REVIVE = "Revive"

SPECIAL_CARDS = [REVIVE, POTION, SLEEPING_PILLS]
SPECIAL_EMOJI = {
    POTION: '❤️‍🔥',
    SLEEPING_PILLS: '💊',
    REVIVE: '🚑',
}
IS_DONATE_EMOJI = '💵'

BLUE_TEAM = '🔹'
RED_TEAM = '🔸'
