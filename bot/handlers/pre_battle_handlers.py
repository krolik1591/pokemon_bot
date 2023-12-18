import asyncio
import os
from pathlib import Path

from aiogram import F, types, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

import bot.menus
from bot.data.const import MAX_ACTIVE_GAMES
from bot.db import db, methods as db
from bot.db.methods import create_pre_battle, update_pre_battle, get_pre_battle
from bot.models.game import Game
from bot.models.player import Player
from bot.utils import game_service
from bot.utils.config_reader import config
from bot.utils.db_service import DbService
from bot.utils.other import get_mention

router = Router()


@router.message(F.chat.type != "private", Text(startswith="/gb "))
async def group_battle(message: types.Message, state: FSMContext):
    print("start group battle")
    available_chats = config.available_chat_ids.split(',')
    if str(message.chat.id) not in available_chats:
        return

    try:
        bet = int(message.text.removeprefix('/gb '))
        if bet <= 0:
            raise ValueError
    except ValueError:
        return await message.answer('Bet must be integer and bigger than 0!')

    err = await pre_game_check(message.from_user.id, message.from_user.first_name, int(bet))
    if err:
        return await message.answer(err)

    players = {
        'blue': [message.from_user.id],
        'red': [],
        str(message.from_user.id): message.from_user.first_name
    }

    pre_battle_id = await create_pre_battle(players)
    players['id'] = pre_battle_id
    await update_pre_battle(pre_battle_id, players)

    text, kb = bot.menus.waiting_menus.waiting_group_battle_menu(bet, players, pre_battle_id)
    image_bytes = get_image_bytes('image1.jpg')

    await message.answer_photo(
        photo=types.BufferedInputFile(image_bytes, filename="image1.png"),
        caption=text,
        reply_markup=kb
    )


@router.callback_query(Text(startswith='group_battle|'))
async def join_group_battle(call: types.CallbackQuery, state: FSMContext):
    print("join group battle")
    _, bet, team, pre_battle_id = call.data.split('|')

    err = await pre_game_check(call.from_user.id, call.from_user.first_name, int(bet))
    if err:
        return await call.message.answer(err)

    players = await get_pre_battle(pre_battle_id)
    if call.from_user.id in players['red'] + players['blue']:
        return await call.answer('You already in this game!')

    if len(players[team]) == 2:
        return await call.answer('This team is full!')

    players[team].append(call.from_user.id)
    players[str(call.from_user.id)] = call.from_user.first_name
    await update_pre_battle(pre_battle_id, players)

    if len(players['blue']) == 2 and len(players['red']) == 2:
        await process_start_game(call, state, players['blue'] + players['red'], int(bet))
        return

    text, kb = bot.menus.waiting_menus.waiting_group_battle_menu(bet, players, pre_battle_id)
    await call.message.edit_caption(caption=text, reply_markup=kb)


@router.message(F.chat.type != "private", Text(startswith="/battle "))
async def start_battle(message: types.Message, state: FSMContext):
    print("start battle")
    available_chats = config.available_chat_ids.split(',')
    if str(message.chat.id) not in available_chats:
        return

    try:
        bet = int(message.text.removeprefix('/battle '))
        if bet <= 0:
            raise ValueError
    except ValueError:
        return await message.answer('Bet must be integer and bigger than 0!')

    err = await pre_game_check(message.from_user.id, message.from_user.first_name, int(bet))
    if err:
        return await message.answer(err)

    text, kb = bot.menus.waiting_menus.waiting_battle_menu(message.from_user, bet)
    image_bytes = get_image_bytes('image1.jpg')

    await message.answer_photo(
        photo=types.BufferedInputFile(image_bytes, filename="image1.png"),
        caption=text,
        reply_markup=kb
    )


@router.callback_query(Text(startswith='join_battle'))
async def join_battle(call: types.CallbackQuery, state: FSMContext):
    _, player_1_id, bet = call.data.split('|')

    player_1_id = int(player_1_id)

    if call.from_user.id == player_1_id:
        return await call.answer('You cannot battle with yourself!')

    bet = int(bet) if bet != 'None' else None
    err = await pre_game_check(call.from_user.id, call.from_user.first_name, bet)
    if err:
        return await call.answer(err)

    players = {
        'blue': [player_1_id],
        'red': [call.from_user.id]
    }

    await process_start_game(call, state, players['blue'] + players['red'], int(bet))


async def process_start_game(call, state, players: [int], bet):
    players1 = []
    players2 = []
    for index, player_id in enumerate(players):
        player_data = await state.bot.get_chat(player_id)

        err = await pre_game_check(player_id, player_data.first_name, bet)
        if err:
            return await call.message.answer(err)

        if index % 2 == 0:
            players1.append(await Player.new(player_data))
        else:
            players2.append(await Player.new(player_data))

    game = Game.new(
        players1 + players2,
        bet=bet,
        chat_id=call.message.chat.id
    )

    game = await game_service.save_game(game)

    await DbService.withdraw_tokens(players, bet, game.game_id)

    await state.update_data(flood_limit=None)

    await call.message.edit_caption(caption='Shuffling cards...')
    await asyncio.sleep(1)
    await call.message.edit_caption(caption='Game started!')
    await asyncio.sleep(1)
    await call.message.delete()

    text, kb = bot.menus.select_menus.select_dogemon_menu(game, first_move=True)
    image_bytes = get_image_bytes('image2.jpg')

    msg = await call.message.answer_photo(
        photo=types.BufferedInputFile(image_bytes, filename="image1.png"),
        caption=text,
        reply_markup=kb
    )

    game.set_msg_id(msg.message_id)
    await game_service.save_game(game)


def get_image_bytes(name):
    path = Path(__file__).parent.parent / 'data' / 'images' / name
    photo_path = os.path.join(path)

    with open(photo_path, "rb") as photo_file:
        return photo_file.read()


async def pre_game_check(player_id, player_name, bet, without_bets=False):
    link = get_mention(player_id, player_name)

    active_games = await db.get_active_games(player_id)
    if len(active_games) >= MAX_ACTIVE_GAMES:
        game_ids = [f"<code>{str(game['_id'])}</code>" for game in active_games]
        return f'{link} have {len(active_games)} games.\n' \
               f'Game ids: \n{", ".join(game_ids)}\n\n' \
               f'Maximum active games: {MAX_ACTIVE_GAMES}\n\n'

    if without_bets or bet is None:
        return None

    user1_balance = await db.get_user_balance(player_id)
    if user1_balance < bet:
        return f"{link} don't have tokens to start a battle!"

    return None
