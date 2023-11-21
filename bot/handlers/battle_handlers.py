import random

from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

from bot.dogemons import DOGEMONS, DOGEMONS_MAP
from bot.menus import battle
from bot.menus.battle_menus import choose_attack_menu, choose_dogemon
from bot.models import game_service
from bot.models.errors import PokemonDead
from bot.models.game import Game
from bot.models.player import Player

router = Router()


@router.message(F.chat.type != "private", Command("battle"))
async def cmd_battle(message: types.Message, state: FSMContext):
    text, kb = battle.waiting_battle_menu(message.from_user)
    await message.answer(text, reply_markup=kb)


@router.callback_query(Text(startswith='join_battle_'))
async def join_battle(call: types.CallbackQuery, state: FSMContext):
    player_1_id = int(call.data.removeprefix('join_battle_'))

    if call.from_user.id == player_1_id:
        return await call.answer('You cannot battle with yourself!')

    players = [
        Player.new(await state.bot.get_chat(player_1_id)),
        Player.new(call.from_user)
    ]
    random.shuffle(players)

    game = Game.new(players[0], players[1])
    game = await game_service.save_game(game)

    text, kb = battle.choose_dogemon(game, first_move=True)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith='choose_dogemon|'))
async def player_choose_dogemon(call: types.CallbackQuery, state: FSMContext):
    _, game_id, pokemon = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_move(call.from_user.id):
        return await call.answer('You cannot select dogemon now!')

    game.select_pokemon(call.from_user.id, pokemon)

    if not game.all_pokemons_selected():
        game.end_move()  # end move ONLY if not all pokemons are selected
        await game_service.save_game(game)

        # show this menu again for another player
        text, kb = battle.choose_dogemon(game)
        return await call.message.edit_text(text, reply_markup=kb)

    # both players selected pokemon
    await game_service.save_game(game)  # save game without end move - the last player to pick a pokemon attacks first

    text, kb = choose_attack_menu(game)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith='fight|'))
async def fight_attack(call: types.CallbackQuery, state: FSMContext):
    _, action, game_id = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_move(call.from_user.id):
        return await call.answer('Not your turn!')

    if action == 'basic_atc':
        game.base_atk()
    elif action == 'power_atk':
        game.power_atk()

    game.end_move()
    await game_service.save_game(game)

    # check next player pokemons
    if not game.check_if_pokemon_alive():

        if not game.have_alive_pokemons():
            winner, loser = game.get_winner_loser()
            text = f'{winner.mention} you are win!'
            await call.message.edit_text(text)
            # todo send money?
            # todo delete game?
            return

        text, kb = choose_dogemon(game)
        return await call.message.edit_text(text, reply_markup=kb)

    # continue battle if pokemons are ok
    text, kb = choose_attack_menu(game)
    await call.message.edit_text(text, reply_markup=kb)



@router.inline_query()
async def inline_send_invite(query: types.InlineQuery, state):
    # InlineKeyboardButton(text=_('REFERRALS_MENU_SEND_INVITE'), switch_inline_query=""),
    await query.answer([types.InlineQueryResultArticle(
        id=query.id,
        title='hi',
        description='im wonna kill you',
        input_message_content=types.InputTextMessageContent(message_text='dont be a pusse'),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
            text='im come destroy ur dogemon.',
            url=await create_start_link(state.bot, str(query.from_user.id)))
        ]]))
    ], cache_time=0, is_personal=True)
