from aiogram import F, Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db import db

router = Router()


# @router.message(F.chat.type != "private", Text("/balance"))
# async def create_user_in_db(message: types.Message, state: FSMContext):
#     exist = await db.is_user_exist(message.from_user.id)
#     if not exist:
#         await message.answer('Please create account in Dr Oak bot first')
#         return
#     return message.answer(await db.get_user_balance(tg_userid=message.from_user.id))