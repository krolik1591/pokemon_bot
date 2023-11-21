from aiogram import F, Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.db import db
from bot.menus.main_menu import main_menu

router = Router()


@router.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    exist = await db.is_user_exist(message.from_user.id)
    if not exist:
        await db.create_new_user(message.from_user.id)

    text, kb = main_menu(message.from_user)
    await message.answer(text, reply_markup=kb)


@router.callback_query(Text('main_menu'))
async def edit_to_main_menu(callback: CallbackQuery):
    message = callback.message
    text, kb = main_menu(message.from_user)
    await message.edit_text(text, reply_markup=kb)
