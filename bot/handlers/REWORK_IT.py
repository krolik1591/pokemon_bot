from bot.db import methods as db


async def check_user_balances(user1, user2, bet):
    user1_balance = await db.get_user_balance(user1.id)
    user2_balance = await db.get_user_balance(user2.id)

    text = []
    if user1_balance < bet:
        text.append(f'{user1.get_mention()} have no money to bet!')
    if user2_balance < bet:
        text.append(f'{user2.get_mention()} have no money to bet!')

    return text
