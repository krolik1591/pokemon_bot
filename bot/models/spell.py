class Spell:
    name: str
    attack: int
    is_defence: bool
    count: int
    emoji: str

    def __init__(self, name, attack, is_defence, count, emoji='🤷🏿‍♀️'):
        self.name = name
        self.atk_power = attack
        self.is_defence = is_defence
        self.count = count
        self.emoji = self.emoji
