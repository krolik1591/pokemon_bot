import random

from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from bot.menus import battle
from bot.menus.battle_menus import battle_menu, choose_dogemon, select_attack
from bot.models import game_service
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

    game.select_pokemon(pokemon)

    if not game.is_all_pokemons_selected():
        game.end_move()  # end move ONLY if not all pokemons are selected
        await game_service.save_game(game)

        # show this menu again for another player
        text, kb = battle.choose_dogemon(game)
        return await call.message.edit_text(text, reply_markup=kb)

    # both players selected pokemon
    await game_service.save_game(game)  # save game without end move - the last player to pick a pokemon attacks first

    text, kb = battle_menu(game)
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith='fight_menu|'))
async def fight_menu(call: types.CallbackQuery, state: FSMContext):
    _, action, game_id = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_move(call.from_user.id):
        return await call.answer('Not your turn!')

    if action == 'attack':
        text, kb = select_attack(game)
        return await call.message.edit_text(text, reply_markup=kb)

    if action == 'special_cards':
        pass

    if action == 'timeout':
        pass

    if action == 'flee':
        pass


@router.callback_query(Text(startswith='fight|'))
async def fight_attack(call: types.CallbackQuery, state: FSMContext):
    _, spell_name, game_id = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_move(call.from_user.id):
        return await call.answer('Not your turn!')

    try:
        game.cast_spell(spell_name)
    except Exception:
        return await call.answer('Cant cast it this round!')

    game.end_move()
    await game_service.save_game(game)

    # check next player pokemons
    if not game.is_all_pokemons_selected():

        is_game_over = game.is_game_over()
        if is_game_over:
            winner, loser = is_game_over
            text = f'{winner.mention} you are win!'
            await call.message.edit_text(text)
            # todo send money?
            # todo delete game?
            return

        text, kb = choose_dogemon(game)
        return await call.message.edit_text(text, reply_markup=kb)

    # continue battle if pokemons are ok
    text, kb = battle_menu(game)
    await call.message.edit_text(text, reply_markup=kb)



