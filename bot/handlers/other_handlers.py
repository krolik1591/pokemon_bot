import math

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link

from bot.data.const import REWARD
from bot.db import db
from bot.REWORK_IT import end_game
from bot.handlers.battle_handlers import get_image_bytes, kick_user
from bot.utils import game_service

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


@router.message(F.chat.type != "private", Command("my_games"))
async def my_games(message: types.Message):
    active_games = await db.get_active_games(message.from_user.id)
    if not active_games:
        await message.answer('There are no active games')
    game_ids = [f"<code>{str(game['_id'])}</code>" for game in active_games]
    mention = markdown.hlink(message.from_user.first_name, create_tg_link("user", id=message.from_user.id))
    await message.answer(f"{mention} games: \n{', '.join(game_ids)}")


@router.message(F.chat.type != "private", Command("cancel"))
async def cancel_games(message: types.Message, state: FSMContext):
    active_games = await db.get_active_games(message.from_user.id)
    if not active_games:
        await message.answer('There are no active games')

    for game in active_games:
        if len(game['players']) == 4:
            continue

        game_id = str(game['_id'])
        game = await game_service.get_game(game_id)
        winner_team, looser_team = game.game_over_coz_flee(message.from_user.id)
        await end_game([winner.id for winner in winner_team], game)

        pool = game.bet * len(game.players) if game.bet else 0
        reward = math.floor(pool * REWARD)

        looser_mention = [looser.mention for looser in looser_team]
        winner_mention = [winner.mention for winner in winner_team]
        text = f'Game msg delete cuz {", ".join(looser_mention)} canceled all games.\n\nWinner: {", ".join(winner_mention)}.\nWinner reward: {reward} $POKECARD.'
        await state.bot.edit_message_caption(caption=text, chat_id=game.chat_id, message_id=game.msg_id)
        await message.answer(f'{", ".join(winner_mention)} win, cuz {", ".join(looser_mention)} canceled all 1x1 games.\n\nWinner reward: {reward} $POKECARD.')

        # if bot admin
        await kick_user(state, game.chat_id, looser_team, winner_team)
