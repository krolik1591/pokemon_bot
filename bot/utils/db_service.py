from datetime import datetime

from bot.data.const import POTION, REVIVE, SLEEPING_PILLS
from bot.db.db import mongodb


class DbService:

    @staticmethod
    async def subtract_special_card(player_id: int, special_card_name: str):
        card = ''
        for to_db, from_db in items_from_db.items():
            if from_db == special_card_name:
                card = to_db
                break
        await mongodb['users'].update_one({'tg_userid': player_id}, {'$inc': {f'items.' + card: -1}})

    @staticmethod
    async def get_purchased_cards(tg_userid: int):
        user = await mongodb['users'].find_one({'tg_userid': tg_userid})
        special_cards = []
        for item, count in user['items'].items():
            if count > 0:
                special_cards.append(items_from_db[item])

        return special_cards

    @staticmethod
    async def withdraw_tokens(player_ids: [int], amount: int, game_id):
        new_withdraw = {'txnHash': game_id, 'value': amount, 'time': datetime.now()}
        await mongodb['users'].update_many({'tg_userid': {'$in': player_ids}}, {'$push': {'withdrawals': new_withdraw}})


items_from_db = {
    'potion': POTION,
    'revive_pill': REVIVE,
    'sleeping_pill': SLEEPING_PILLS,
}
