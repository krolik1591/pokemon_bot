from pprint import pprint

from bson import ObjectId
from datetime import datetime

from bot.db.db import mongodb
from functools import reduce 

# USERS

async def is_user_exist(tg_userid):
    user = await mongodb['users'].find_one({'tg_userid': tg_userid})
    return bool(user)

# GAME


async def create_new_game(game_info):
    game = await mongodb['games'].insert_one(game_info)
    return game.inserted_id


async def get_game_by_id(game_id):
    game_id = ObjectId(game_id)
    game = await mongodb['games'].find_one({'_id': game_id})
    return game


async def update_game(game_id, game_info):
    game_id = ObjectId(game_id)
    await mongodb['games'].update_one(
        {
            '_id': game_id
        },
        {
            '$set': game_info
        }
    )
import pymongo

# REWORK IT
async def get_exclusive_winners(): 
    docs = mongodb['winners'].find().sort("wins", pymongo.DESCENDING).limit(10)
    winners = []
    async for doc in docs: 
        winners.append(doc)
    return winners

async def get_user_balance(tg_userid):
    user = await mongodb['users'].find_one({ "tg_userid": tg_userid})
    
    total_deposit = reduce(lambda total, deposit: total + deposit['value'], user['deposits'], 0) if user['deposits'] else 0

    total_withdrawals = reduce(lambda total, withdrawal: total + withdrawal['value'], user['withdrawals'], 0) if user['withdrawals'] else 0
    
    token_withdrawals = reduce(lambda total, withdrawal: total + withdrawal['value'], user['tokenWithdrawals'], 0) if user['tokenWithdrawals'] else 0

    balance = total_deposit - (total_withdrawals + token_withdrawals)
    
    return balance if balance is not None else 0


async def get_game(game_id_obj):
    game_id_obj = ObjectId(game_id_obj)
    game = await mongodb['games'].find_one({
        '_id': game_id_obj
    })
    return game


async def get_active_games(tg_userid):
    game = await mongodb['games'].find({
        '$or': [
            {'player1.id': tg_userid},
            {'player2.id': tg_userid}
        ],
        'winner': None
    },
        sort=[('creation_time', -1)]).to_list(length=None)
    return game


async def update_user_balance(tg_userid, balance_to_add):
    await mongodb['users'].update_one(
        {
            'tg_userid': tg_userid
        },
        {
            '$inc': {
                'balance': balance_to_add
            }
        }
    )


async def deposit_tokens(tg_userid, amount, game_id = str(10000)):
    new_deposit = { 'txnHash': game_id, 'value': amount, 'time':  datetime.now()}
    await mongodb['users'].update_one(
        {
            'tg_userid': tg_userid
        },
        {
            '$push': {
                "deposits" : new_deposit
            }
        }
    )


async def deposit_burn(amount): 
    new_deposit = { 'txnHash': "10000", 'value': amount, 'time': datetime.now()}
    await mongodb['users'].update_one(
        {
            'tg_userid': 99999 
        },
        {
            "$push": {
                "deposits": new_deposit
            }
        }
    )


async def withdraw_tokens(tg_userid, amount, game_id = str(10000)):
    new_withdraw = { 'txnHash': game_id, 'value': amount, 'time':  datetime.now()}
    await mongodb['users'].update_one(
        {
            'tg_userid': tg_userid
        },
        {
            '$push': {
                "withdrawals" : new_withdraw
            }
        }
    )


async def increase_exclusive_win(tg_userid): 
    user = await mongodb['winners'].find_one({
        'userid': tg_userid
    })

    if user == None:
        existing_user = await mongodb['users'].find_one({
            'tg_userid': tg_userid
        })

        await mongodb['winners'].insert_one({
            'userid': tg_userid,
            'wins': 1,
            'name': existing_user['name'],
            'username': existing_user['username']
        })
    else: 
        await mongodb['winners'].update_one(
            {
                'userid': tg_userid
            },
            {
                '$inc': {
                    'wins': 1 
                }
            }
        )


if __name__ == '__main__':
    import asyncio

    async def main():
        # x = await get_active_game(357108179)
        x = await get_active_games(357108179)
        pprint(str(x[0]['_id']))


    asyncio.run(main())
