import random
from pprint import pprint

from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

from bot.db import db
from bot.dogemons import DOGEMONS, DOGEMONS_MAP, DOGEMON_1, DOGEMON_2
from bot.menus.battle_menus import choose_attack_menu, choose_battle_dogemon_menu, special_attack_menu
from bot.models import game_service
from bot.models.game import Game
from bot.menus import battle

router = Router()


@router.callback_query(Text('choose_battle_dogemon_menu'))
async def choose_battle_dogemon(call: types.CallbackQuery, state: FSMContext):
    text, kb = choose_battle_dogemon_menu(call.from_user, DOGEMONS)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith='battle_dogeMON_'))
async def choose_attack(call: types.CallbackQuery, state: FSMContext):
    dogemon_name = call.data.removeprefix('battle_dogeMON_')

    dogemon_info = find_dogemon_info(dogemon_name)
    enemy_dogemon_info = find_enemy_dogemon_info()

    game = Game
    text, kb = choose_attack_menu(call.from_user, game)
    await call.message.edit_text(text, reply_markup=kb)


@router.message(F.chat.type != "private", Command("battle"))
async def cmd_battle(message: types.Message, state: FSMContext):
    text, kb = battle.waiting_battle_menu(message.from_user)
    await state.bot.send_message(message.chat.id, text, reply_markup=kb)


@router.callback_query(Text(startswith='join_battle_'))
async def join_battle(call: types.CallbackQuery, state: FSMContext):
    player_1 = int(call.data.removeprefix('join_battle_'))
    if call.from_user.id == player_1:
        await call.answer('You cannot battle with yourself!')
        return
    player_2 = call.from_user.id

    first_move = random.choice([player_1, player_2])
    if first_move == player_1:
        game = Game.new(player_1, player_2)

        users_tg = await state.bot.get_chat(player_1)
        username = users_tg.username
    else:
        username = call.from_user.username
        game = Game.new(player_2, player_1)

    game_id = await db.create_new_game(game.to_mongo())

    text, kb = battle.choose_dogemon1(username, game_id)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith='player1_choose_dogemon|'))
async def player1_choose_dogemon(call: types.CallbackQuery, state: FSMContext):
    _, game_id, pokemon1 = call.data.split('|')

    game = await game_service.get_game(game_id)

    if call.from_user.id != game.player1:
        await call.answer('You cannot choose dogemon for your opponent!')
        return

    game.select_pokemon(game.player1, pokemon1)

    info = await state.bot.get_chat(game.player2)
    username = info.username

    await game_service.save_game(game)

    text, kb = battle.choose_dogemon2(username, game_id)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith='player2_choose_dogemon|'))
async def player2_choose_dogemon(call: types.CallbackQuery, state: FSMContext):
    _, game_id, pokemon2 = call.data.split('|')

    game_json = await db.get_game_by_id(game_id)
    game = Game.from_mongo(game_json)

    if call.from_user.id != game.player2:
        await call.answer('You cannot choose dogemon for your opponent!')
        return

    game.select_pokemon(game.player2, pokemon2)

    text, kb = special_attack_menu(call.from_user, game)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith='fight|'))
async def fight_attack(call: types.CallbackQuery, state: FSMContext):

    _, action, game_id = call.data.split('|')

    # todo get game by game id from mongo
    # construct Game instance
    # check if player can move
        # fuck player if not
    # if action == "base_atk":
    #   game.base_atk()
    # ... so on

    # save game


    dogemon_name = call.data.removeprefix('battle_dogeMON_')

    dogemon_info = find_dogemon_info(dogemon_name)
    enemy_dogemon_info = find_enemy_dogemon_info()

    text, kb = special_attack_menu(call.from_user, dogemon_info, enemy_dogemon_info)
    await call.message.edit_text(text, reply_markup=kb)


@router.inline_query()
async def inline_send_invite(query: types.InlineQuery, state):
    # InlineKeyboardButton(text=_('REFERRALS_MENU_SEND_INVITE'), switch_inline_query=""),
    await query.answer([types.InlineQueryResultArticle(
        title='hi', description='im wonna kill you',
        id=query.id, input_message_content=types.InputTextMessageContent(
            message_text='dont be a pusse'),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text='im come destroy ur dogemon.',
                                       url=await create_start_link(state.bot, str(query.from_user.id)))
        ]]))
    ], cache_time=0, is_personal=True)


def find_dogemon_info(name):
    return DOGEMONS_MAP[name]


def find_enemy_dogemon_info():
    return random.choice(DOGEMONS)
