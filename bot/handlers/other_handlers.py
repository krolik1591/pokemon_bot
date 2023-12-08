from aiogram import F, Router, types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.handlers.battle_handlers import get_image_bytes

router = Router()


@router.message(F.chat.type == "private", Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    text = "Welcome to <b><i>PokéCards Game Bot!</i></b> The first ever PvP betting Pokémon inspired Cards game on telegram.\n\n" \
           "Please start by linking your wallet by sending set command to @pokecardsdexbot and start your Battles in the official group.\n\n" \
           "/set <i>wallet_address</i>\n" \
           "/battle <i>amount</i> - start a Battle with wager"
    image_bytes = get_image_bytes('start_image.png')

    await message.answer_photo(
        photo=types.BufferedInputFile(image_bytes, filename="start_image.png"),
        caption=text,
    )
