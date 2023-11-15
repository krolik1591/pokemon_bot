from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.db import db
from bot.menus.battle_menus import choose_battle_dogemon_menu
from bot.menus.main_menu import main_menu
from utils.utils import get_username_or_link

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


