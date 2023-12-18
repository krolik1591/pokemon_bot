import asyncio
import math
import time

from aiogram import Router, exceptions, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

import bot.menus.select_menus
import bot.menus.waiting_menus
from bot.data import const
from bot.data.const import REWARD, PRIZE_POOL, MAX_USES_OF_SPECIAL_CARDS, IS_DONATE_EMOJI
from bot.db import db, methods as db
from bot.menus.battle_menus import battle_menu
from bot.menus.special_menus import special_cards_menu, revive_pokemon_menu
from bot.menus.select_menus import select_dogemon_menu, select_attack_menu
from bot.models.game import Game
from bot.utils import game_service
from bot.models.player import Player
from bot.utils.config_reader import config
from bot.utils.other import special_by_emoji

router = Router()


@router.callback_query(Text(startswith='select_dogemon_menu|'))
async def player_select_dogemon(call: types.CallbackQuery, state: FSMContext):
    flood_limit = (await state.get_data()).get('flood_limit')
    if flood_limit:
        return await call.answer(f'Wait {int(flood_limit - time.time())} seconds!!!')

    _, pokemon, game_id, who_next_move = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('You cannot select PokéCards now!')

    # need to working `BACK` button
    if pokemon != 'None':
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
    if len(who_next_move) == 1:
        game.who_move = int(who_next_move)
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
    print('who move', game.who_move)

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
        await process_end_game(call, state, game, win_type='flee')
        return


@router.callback_query(Text(startswith='fight|'))
async def fight_attack(call: types.CallbackQuery, state: FSMContext):
    flood_limit = (await state.get_data()).get('flood_limit')
    if flood_limit:
        return await call.answer(f'Wait {int(flood_limit - time.time())} seconds!!!')

    _, is_special, item_name, game_id, defender_index = call.data.split('|')

    game = await game_service.get_game(game_id)

    if not game.is_player_attacks_now(call.from_user.id):
        return await call.answer('Not your turn!')

    try:
        if is_special == "T":
            is_donate = True if item_name.endswith(IS_DONATE_EMOJI) else False
            item_name = item_name.removesuffix(IS_DONATE_EMOJI) if is_donate else item_name
            special_name = special_by_emoji(item_name)

            to_revive = game.get_attacker().get_pokemons_to_revive()
            if item_name in to_revive and defender_index == 'None':
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
            actions = game.cast_spell(item_name, defender_index)
            game.end_move()

    except Exception as ex:
        return await call.answer('Cant cast it this round! ' + str(ex))

    who_next_move = game.who_move
    await game_service.save_game(game)

    # check next player pokemons
    if not game.is_all_pokemons_selected():

        is_game_over = game.is_game_over()
        if is_game_over:
            await process_end_game(call, state, game, win_type='clear')
            return

        player = game.player_need_choose_pokemon()
        if not any(is_alive for pokemon, is_alive in player.pokemons_pool.items()):
            text, kb = battle_menu(game, latest_actions=actions)
            await try_to_edit_caption(call, state, text, kb)
            return
        game.set_attacker(game.players.index(player))
        await game_service.save_game(game)
        text, kb = select_dogemon_menu(game, latest_actions=actions, who_next_move=who_next_move)
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


async def process_end_game(call, state, game, win_type):
    pool = game.bet * len(game.players) if game.bet else 0
    reward = math.floor(pool * REWARD)
    burnt = math.floor(pool * PRIZE_POOL)

    if win_type == 'flee':
        winner_team, looser_team = game.game_over_coz_flee(call.from_user.id)
        text = f'{to_mention(winner_team)} won {reward} $POKECARD while {to_mention(looser_team)} fled the battle and {burnt} will be burnt'
    elif win_type == 'clear':
        looser_team, winner_team = game.get_attacker_defencer_team()
        text = f'{to_mention(winner_team)} won {reward} $POKECARD. {to_mention(looser_team)} has no PokéCards left'
    elif win_type == 'timeout':
        winner_team, looser_team = game.is_game_over_coz_timeout()
        text = f"{to_mention(winner_team)} won {reward} $POKECARD while {to_mention(looser_team)} was inactive"
    else:
        raise ValueError(f'Unknown loose_type: {win_type}')

    await try_to_edit_caption(call, state, text, kb=None)
    await end_game([winner.id for winner in winner_team], game)

    # if bot is admin
    await kick_user(state, call.message.chat.id, looser_team, winner_team)


async def end_game(winner_ids: [int], game: Game):
    await db.update_game(game.game_id, {'winner': winner_ids})

    if game.bet is None:
        return
    coef = len(game.players)
    for_winner = game.bet * coef * REWARD
    prize_pool = game.bet * coef * PRIZE_POOL

    await db.deposit_tokens(winner_ids, for_winner/len(winner_ids))
    await db.deposit_burn(prize_pool)


def to_mention(team):
    return ', '.join([player.mention for player in team])


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
