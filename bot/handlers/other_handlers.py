from aiogram import F, Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db import db

router = Router()


@router.message(F.chat.type != "private", Text("/hi"))
async def create_user_in_db(message: types.Message, state: FSMContext):
    exist = await db.is_user_exist(message.from_user.id)
    if not exist:
        await db.create_new_user(message.from_user.id)
        await message.answer('User created! You has 100 coins')
        return
    return await message.answer('User already exist!')