import asyncio
import os
from pathlib import Path

from aiogram import F, Router, exceptions, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.handlers.REWORK_IT import pre_game_check, end_game, take_money_from_players
from bot.menus import battle
from bot.menus.battle_menus import battle_menu, revive_pokemon_menu, select_dogemon_menu, select_attack_menu, \
    special_cards_menu
from bot.utils import game_service
from bot.models.game import Game
from bot.models.player import Player

router = Router()


@router.message(F.chat.type != "private", Command("battle_fun"))
async def fun_battle(message: types.Message):
    err = await pre_game_check(message.from_user.id, None, without_bets=True)
    if err:
        return await message.answer(err)

    text, kb = battle.waiting_battle_menu(message.from_user, None)
    image_bytes = get_image_bytes('image1.jpg')

    await message.answer_photo(
        photo=types.BufferedInputFile(image_bytes, filename="image1.png"),
        caption=text,
        reply_markup=kb
    )


@router.message(F.chat.type != "private", Text(startswith="/battle "))
async def money_battle(message: types.Message, state: FSMContext):
    try:
        bet = int(message.text.removeprefix('/battle '))
        if bet <= 0:
            raise ValueError
    except ValueError:
        return await message.answer('Bet must be integer and bigger than 0!')

    err = await pre_game_check(message.from_user.id, int(bet))
    if err:
        return await message.answer(err)

    text, kb = battle.waiting_battle_menu(message.from_user, bet)
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
    err = await pre_game_check(call.from_user.id, bet)
    if err:
        return await call.answer(err)

    if bet is not None:
        await take_money_from_players(player_1_id, call.from_user.id, bet)

    game = Game.new(
        Player.new(await state.bot.get_chat(player_1_id)),
        Player.new(call.from_user),
        bet=bet,
    )

    game = await game_service.save_game(game)

    await call.message.edit_caption(caption='Shuffling cards...')
    await asyncio.sleep(1)
    await call.message.edit_caption(caption='Game started!')
    await asyncio.sleep(1)
    await call.message.delete()

    text, kb = battle.select_dogemon_menu(game, first_move=True)
    image_bytes = get_image_bytes('image2.jpg')

    await call.message.answer_photo(
        photo=types.BufferedInputFile(image_bytes, filename="image1.png"),
        caption=text,
        reply_markup=kb
    )


@router.callback_query(Text(startswith='select_dogemon_menu|'))
async def player_select_dogemon(call: types.CallbackQuery, state: FSMContext):
    _, pokemon, game_id = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('You cannot select dogemon now!')

    # need to working `BACK` button
    if pokemon != 'None':
        game.select_pokemon(pokemon)

    if not game.is_all_pokemons_selected():
        game.end_move()  # end move ONLY if not all pokemons are selected
        await game_service.save_game(game)

        # show this menu again for another player
        text, kb = battle.select_dogemon_menu(game)
        return await call.message.edit_caption(caption=text, reply_markup=kb)

    # both players selected pokemon
    if pokemon != 'None':
        game.end_move()
    await game_service.save_game(game)  # save game without end move - the last player to pick a pokemon attacks first

    text, kb = battle_menu(game)
    await call.message.edit_caption(caption=text, reply_markup=kb)


@router.callback_query(Text(startswith='fight_menu|'))
async def fight_menu(call: types.CallbackQuery, state: FSMContext):
    _, action, game_id = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('Not your turn!')

    if action == 'attack':
        kb = select_attack_menu(game)
        await try_to_edit_reply_markup(call, kb)
        return

    if action == 'special_cards':
        if not game.get_attacker().special_card:
            return await call.answer('You have no special cards!')
        kb = special_cards_menu(game)
        await try_to_edit_reply_markup(call, kb)
        return

    if action == 'flee':
        await process_end_game(call, state, game)


async def process_end_game(call, state, game, is_timeout=False):
    if is_timeout:
        winner, looser = game.is_game_over_coz_timeout()
    else:
        looser, winner = game.get_attacker_defencer()

    db_game = await db.get_active_game(winner.id)
    reward = db_game['bet'] * 2 if db_game['bet'] else 0

    text = f'{winner.mention} won {reward} {winner.pokemon.name} while {looser.mention} fled the battle'
    await try_to_edit_caption(call, text, kb=None)
    # await call.message.edit_caption(caption=text)

    await end_game(winner.id, game)

    # if bot is admin
    await kick_user(state, call.message.chat.id, looser)


@router.callback_query(Text(startswith='fight|'))
async def fight_attack(call: types.CallbackQuery, state: FSMContext):
    _, is_special, item_name, game_id = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('Not your turn!')

    try:
        if is_special == "True":
            actions = game.use_special_card(item_name)
        else:
            actions = game.cast_spell(item_name)
            game.end_move()

    except Exception as ex:
        return await call.answer('Cant cast it this round! ' + str(ex))

    await game_service.save_game(game)

    # check next player pokemons
    if not game.is_all_pokemons_selected():

        is_game_over = game.is_game_over()
        if is_game_over:
            await process_end_game(call, state, game)

        text, kb = select_dogemon_menu(game, latest_actions=actions)
        return await call.message.edit_caption(caption=text, reply_markup=kb)

    # continue battle if pokemons are ok
    text, kb = battle_menu(game, latest_actions=actions)
    await try_to_edit_caption(call, text, kb)


@router.callback_query(Text(startswith='revive_pokemon|'))
async def fight_attack(call: types.CallbackQuery):
    _, game_id = call.data.split('|')
    game = await game_service.get_game(game_id)

    pokemons_to_revive = game.get_attacker().get_pokemons_to_revive()

    if not pokemons_to_revive:
        return await call.answer("All pokemons are alive!")

    text, kb = revive_pokemon_menu(game, pokemons_to_revive)
    await call.message.edit_caption(caption=text, reply_markup=kb)


@router.callback_query(Text(startswith='timeout|'))
async def timeout(call: types.CallbackQuery, state: FSMContext):
    _, game_id = call.data.split('|')
    game = await game_service.get_game(game_id)

    _, defender = game.get_attacker_defencer()
    if call.from_user.id != defender.id:
        return await call.answer('Only defender can use this btn')

    winner, looser = game.is_game_over_coz_timeout()
    if winner:
        await process_end_game(call, state, game, is_timeout=True)

    await call.answer()



async def try_to_edit_caption(call, text, kb):
    try:
        if kb is not None:
            await call.message.edit_caption(caption=text, reply_markup=kb)
        else:
            await call.message.edit_caption(caption=text)
    except exceptions.TelegramRetryAfter as ex:
        print(f'Too many requests, wait {ex.retry_after} seconds')
        await asyncio.sleep(ex.retry_after)
        await call.message.edit_caption(caption=text, reply_markup=kb)


async def try_to_edit_reply_markup(call, kb):
    try:
        await call.message.edit_reply_markup(reply_markup=kb)
    except exceptions.TelegramRetryAfter as ex:
        print(f'Too many requests, wait {ex.retry_after} seconds')
        await asyncio.sleep(ex.retry_after)
        await call.message.edit_reply_markup(reply_markup=kb)


async def kick_user(state, chat_id, looser):
    try:
        await state.bot.ban_chat_member(chat_id, looser.id)
        await state.bot.unban_chat_member(chat_id, looser.id)

        await state.bot.send_message(chat_id, f'User {looser.mention} loosed and was kicked!')
    except exceptions.TelegramBadRequest:
        print('Im not a admin!')


def get_image_bytes(name):
    path = Path(__file__).parent.parent / 'data' / 'images' / name
    photo_path = os.path.join(path)

    with open(photo_path, "rb") as photo_file:
        return photo_file.read()
