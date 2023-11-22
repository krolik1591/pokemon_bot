TOTAL_SYMBOLS = 10
F1, F2, F3, EMPTY = "🟥", "🟧", "🟩", " .. "  # red yellow green empty


def hp_bar(hp, max_hp):
    hp_percent = hp / max_hp

    filled_symbols_count = round(TOTAL_SYMBOLS * hp_percent)
    empty_symbols_count = TOTAL_SYMBOLS - filled_symbols_count
    filled_symbol = _get_symbol(hp_percent)

    bar = (filled_symbol * filled_symbols_count) + (EMPTY * empty_symbols_count)
    return f"HP: [{bar}] {hp} / {max_hp}"


def _get_symbol(hp_percent):
    if hp_percent > 0.6:
        return F3
    if hp_percent > 0.3:
        return F2
    return F1

