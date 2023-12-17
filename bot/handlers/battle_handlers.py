import asyncio
import math
import os
import time
from pathlib import Path
from pprint import pprint

from aiogram import F, Router, exceptions, types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import bot.menus.select_menus
import bot.menus.waiting_menus
from bot.data import const
from bot.data.const import REWARD, PRIZE_POOL, MAX_USES_OF_SPECIAL_CARDS, IS_DONATE_EMOJI
from bot.db import db
from bot.REWORK_IT import pre_game_check, end_game, take_money_from_players
from bot.menus import battle
from bot.menus.battle_menus import battle_menu
from bot.menus.special_menus import special_cards_menu, revive_pokemon_menu
from bot.menus.select_menus import select_dogemon_menu, select_attack_menu
from bot.utils import game_service
from bot.models.game import Game
from bot.models.player import Player
from bot.utils.config_reader import config
from bot.utils.other import special_by_emoji

router = Router()


@router.message(F.chat.type != "private", Text(startswith="/gb "))
async def group_battle(message: types.Message, state: FSMContext):
    print("start group battle")
    # available_chats = config.available_chat_ids.split(',')
    # if str(message.chat.id) not in available_chats:
    #     return

    try:
        bet = int(message.text.removeprefix('/gb '))
        if bet <= 0:
            raise ValueError
    except ValueError:
        return await message.answer('Bet must be integer and bigger than 0!')

    err = await pre_game_check(message.from_user, int(bet))
    if err:
        return await message.answer(err)

    players = {
        'blue': [message.from_user],
        'red': []
    }
    await state.update_data(players=players)

    text, kb = bot.menus.waiting_menus.waiting_group_battle_menu(bet, players)
    image_bytes = get_image_bytes('image1.jpg')

    await message.answer_photo(
        photo=types.BufferedInputFile(image_bytes, filename="image1.png"),
        caption=text,
        reply_markup=kb
    )


@router.callback_query(Text(startswith='group_battle|'))
async def join_group_battle(call: types.CallbackQuery, state: FSMContext):
    print("join group battle")
    _, bet, team = call.data.split('|')

    err = await pre_game_check(call.from_user, int(bet))
    if err:
        return await call.message.answer(err)

    players: {[call.from_user]} = (await state.get_data()).get('players')
    players[team].append(call.from_user)
    await state.update_data(players=players)

    if len(players['blue']) == 2 and len(players['red']) == 2:
        await process_start_game(call, state, players, int(bet))
        return

    text, kb = bot.menus.waiting_menus.waiting_group_battle_menu(bet, players)
    await call.message.edit_caption(caption=text, reply_markup=kb)


@router.message(F.chat.type != "private", Text(startswith="/battle "))
async def start_battle(message: types.Message, state: FSMContext):
    print("start battle")
    # available_chats = config.available_chat_ids.split(',')
    # if str(message.chat.id) not in available_chats:
    #     return

    try:
        bet = int(message.text.removeprefix('/battle '))
        if bet <= 0:
            raise ValueError
    except ValueError:
        return await message.answer('Bet must be integer and bigger than 0!')

    err = await pre_game_check(message.from_user, int(bet))
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
    err = await pre_game_check(call.from_user, bet)
    if err:
        return await call.answer(err)

    if bet is not None:
        await take_money_from_players(player_1_id, call.from_user.id, bet)

    players = {
        'blue': [await state.bot.get_chat(player_1_id)],
        'red': [call.from_user]
    }
    await process_start_game(call, state, players, int(bet))


@router.callback_query(Text(startswith='select_dogemon_menu|'))
async def player_select_dogemon(call: types.CallbackQuery, state: FSMContext):
    flood_limit = (await state.get_data()).get('flood_limit')
    if flood_limit:
        return await call.answer(f'Wait {int(flood_limit - time.time())} seconds!!!')

    _, pokemon, game_id, change_first_move = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('You cannot select PokéCards now!')

    # need to working `BACK` button
    if pokemon != 'None':
        print([player.pokemon for player in game.players])
        game.select_pokemon(pokemon)

    if not game.is_all_pokemons_selected():
        game.end_move()  # end move ONLY if not all pokemons are selected
        await game_service.save_game(game)

        # show this menu again for another player
        text, kb = bot.menus.select_menus.select_dogemon_menu(game)
        await try_to_edit_caption(call, state, text, kb)
        return

    # both players selected pokemon
    if pokemon != 'None':
        game.end_move()
    if change_first_move == 'True':
        game.end_move()
    await game_service.save_game(game)  # save game without end move - the last player to pick a pokemon attacks first

    text, kb = battle_menu(game)
    await try_to_edit_caption(call, state, text, kb)


@router.callback_query(Text(startswith='fight_menu|'))
async def fight_menu(call: types.CallbackQuery, state: FSMContext):
    flood_limit = (await state.get_data()).get('flood_limit')
    if flood_limit:
        return await call.answer(f'Wait {int(flood_limit - time.time())} seconds!!!')

    _, action, game_id = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('Not your turn!')

    if action == 'attack':
        kb = select_attack_menu(game)
        return await try_to_edit_reply_markup(call, state, kb)

    if action == 'special_cards':
        attacker = game.get_attacker()
        if attacker.uses_of_special_cards >= MAX_USES_OF_SPECIAL_CARDS:
            return await call.answer(f'Maximum number of special cards used! ({MAX_USES_OF_SPECIAL_CARDS})')

        available_donat_cards = await game.db_service.get_purchased_cards(attacker.id)
        used_purchase_special = attacker.used_purchased_special_cards
        donate_special = [card for card in available_donat_cards if card not in used_purchase_special]

        if len(attacker.special_cards) == 0 and len(donate_special) == 0:
            return await call.answer('You have no special cards!')

        kb = special_cards_menu(game, donate_special)
        await try_to_edit_reply_markup(call, state, kb)
        return

    if action == 'flee':
        return await process_end_game(call, state, game, win_type='flee')


@router.callback_query(Text(startswith='fight|'))
async def fight_attack(call: types.CallbackQuery, state: FSMContext):
    flood_limit = (await state.get_data()).get('flood_limit')
    if flood_limit:
        return await call.answer(f'Wait {int(flood_limit - time.time())} seconds!!!')
    print(call.data.split('|'))
    _, is_special, item_name, game_id, defender_index = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('Not your turn!')

    try:
        if is_special == "T":
            is_donate = True if item_name.endswith(IS_DONATE_EMOJI) else False
            item_name = item_name.removesuffix(IS_DONATE_EMOJI) if is_donate else item_name
            special_name = special_by_emoji(item_name)

            if special_name == const.REVIVE and defender_index == 'None':
                actions = await game.revive_pokemon(special_name, is_donate)

            elif special_name == const.SLEEPING_PILLS or defender_index != 'None':
                if defender_index == 'None':
                    kb = bot.menus.select_menus.select_defender_menu(game, special_name, is_special='T', is_donate=is_donate)
                    await try_to_edit_reply_markup(call, state, kb)
                    return
                actions = await game.use_sleeping_pills(defender_index, is_donate)

            elif special_name == const.POTION:
                actions = await game.use_potion(special_name, is_donate)

            else:
                raise Exception('Unknown special card!')
        else:
            attacker = game.get_attacker()
            spell = attacker.pokemon.get_spell_by_name(item_name)
            if not spell.is_defence:
                if defender_index == 'None':
                    kb = bot.menus.select_menus.select_defender_menu(game, item_name, is_special='F')
                    await try_to_edit_reply_markup(call, state, kb)
                    return
            print([player.pokemon.name for player in game.players])
            actions = game.cast_spell(item_name, defender_index)
            game.end_move()

    except Exception as ex:
        return await call.answer('Cant cast it this round! ' + str(ex))

    await game_service.save_game(game)

    # check next player pokemons
    if not game.is_all_pokemons_selected():

        is_game_over = game.is_game_over()
        if is_game_over:
            await process_end_game(call, state, game, win_type='clear')
            return

        text, kb = select_dogemon_menu(game, latest_actions=actions, change_first_move=True)
        return await try_to_edit_caption(call, state, text, kb)

    # continue battle if pokemons are ok
    text, kb = battle_menu(game, latest_actions=actions)
    await try_to_edit_caption(call, state, text, kb)


@router.callback_query(Text(startswith='revive_pokemon'))
async def fight_attack(call: types.CallbackQuery, state: FSMContext):
    flood_limit = (await state.get_data()).get('flood_limit')
    if flood_limit:
        return await call.answer(f'Wait {int(flood_limit - time.time())} seconds!!!')

    action, game_id = call.data.split('|')
    game = await game_service.get_game(game_id)

    is_donate = False
    if action.endswith(IS_DONATE_EMOJI):
        is_donate = True

    pokemons_to_revive = game.get_attacker().get_pokemons_to_revive()

    if not pokemons_to_revive:
        return await call.answer("All pokemons are alive!")

    text, kb = revive_pokemon_menu(game, pokemons_to_revive, is_donate)
    await try_to_edit_caption(call, state, text, kb)


@router.callback_query(Text(startswith='timeout|'))
async def timeout(call: types.CallbackQuery, state: FSMContext):
    flood_limit = (await state.get_data()).get('flood_limit')
    if flood_limit:
        return await call.answer(f'Wait {int(flood_limit - time.time())} seconds!!!')

    _, game_id = call.data.split('|')
    game = await game_service.get_game(game_id)

    _, defender_team = game.get_attacker_defencer_team()

    if call.from_user.id not in [player.id for player in defender_team]:
        return await call.answer('Only defender can use this btn')

    winner, looser = game.is_game_over_coz_timeout()
    if winner:
        await process_end_game(call, state, game, win_type='timeout')

    await call.answer()


@router.callback_query(Text(startswith='cancel_battle'))
async def cancel_battle(call: types.CallbackQuery, state: FSMContext):
    _, who_started = call.data.split('|')
    if call.from_user.id != int(who_started):
        return await call.answer("It's not your msg!")

    await call.message.delete()


async def process_start_game(call, state, players, bet):
    players1 = []
    players2 = []
    for index, player in enumerate(players['blue'] + players['red']):
        if index % 2 == 0:
            players1.append(await Player.new(player))
        else:
            players2.append(await Player.new(player))

    game = Game.new(
        players1 + players2,
        bet=bet,
        chat_id=call.message.chat.id
    )

    game = await game_service.save_game(game)

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


async def process_end_game(call, state, game, win_type):
    db_game = await db.get_game(game.game_id)
    pool = db_game['bet'] * 2 if db_game['bet'] else 0
    reward = math.floor(pool * REWARD)
    burnt = math.floor(pool * PRIZE_POOL)

    if win_type == 'flee':
        winner_team, looser_team = game.game_over_coz_flee(call.from_user.id)
        winners = '\n'.join([player.mention for player in winner_team])
        loosers = '\n'.join([player.mention for player in looser_team])
        text = f'{winners} won {reward} $POKECARD while {loosers} fled the battle and {burnt} will be burnt'
    elif win_type == 'clear':
        looser_team, winner_team = game.get_attacker_defencer_team()
        winners = '\n'.join([player.mention for player in winner_team])
        loosers = '\n'.join([player.mention for player in looser_team])
        text = f'{winners} won {reward} $POKECARD. {loosers} has no PokéCards left'
    elif win_type == 'timeout':
        winner_team, looser_team = game.is_game_over_coz_timeout()
        winners = '\n'.join([player.mention for player in winner_team])
        loosers = '\n'.join([player.mention for player in looser_team])
        text = f"{winners} won {reward} $POKECARD while {loosers} was inactive"
    else:
        raise ValueError(f'Unknown loose_type: {win_type}')

    await try_to_edit_caption(call, state, text, kb=None)
    await end_game([winner.id for winner in winner_team], game)

    # if bot is admin
    await kick_user(state, call.message.chat.id, looser_team, winner_team)


async def try_to_edit_caption(call, state, text, kb):
    try:
        if kb is not None:
            await call.message.edit_caption(caption=text, reply_markup=kb)
        else:
            await call.message.edit_caption(caption=text)
    except exceptions.TelegramRetryAfter as ex:
        print(f'Too many requests, wait {ex.retry_after} seconds')

        await state.update_data(flood_limit=ex.retry_after + time.time())
        await asyncio.sleep(ex.retry_after)
        await state.update_data(flood_limit=None)

        if kb is not None:
            await call.message.edit_caption(caption=text, reply_markup=kb)
        else:
            await call.message.edit_caption(caption=text)


async def try_to_edit_reply_markup(call, state, kb):
    try:
        await call.message.edit_reply_markup(reply_markup=kb)
    except exceptions.TelegramRetryAfter as ex:
        print(f'Too many requests, wait {ex.retry_after} seconds')

        await state.update_data(flood_limit=ex.retry_after + time.time())
        await asyncio.sleep(ex.retry_after)
        await state.update_data(flood_limit=None)

        await call.message.edit_reply_markup(reply_markup=kb)


async def kick_user(state, chat_id, loosers: [Player], winners: [Player]):
    try:
        for looser in loosers:
            await state.bot.ban_chat_member(chat_id, looser.id)
        for winner in winners:
            await db.increase_exclusive_win(winner.id)

        main_chat = config.available_chat_ids.split(',')
        exclusive_winners = await db.get_exclusive_winners()

        formatted_winners = []
        for winner in exclusive_winners:
            link = f"https://t.me/{winner['username']}"
            formatted_winners.append(f"<a href='{link}'>{winner['name']}</a> - {winner['wins']}")

        await state.bot.send_message(int(main_chat[0]), '<b>Exclusive Winners</b>\n\n' + '\n'.join(formatted_winners),
                                     disable_web_page_preview=True, parse_mode="HTML")
        await state.bot.send_message(chat_id, f"User {', '.join(loosers)} lost and was kicked!")
    except exceptions.TelegramBadRequest:
        print('Im not a admin!')


def get_image_bytes(name):
    path = Path(__file__).parent.parent / 'data' / 'images' / name
    photo_path = os.path.join(path)

    with open(photo_path, "rb") as photo_file:
        return photo_file.read()
