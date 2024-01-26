from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from logic.menu import main_menu_handler
from utils import states, request

start = Router()


@start.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()
    status, data = await request.user.get(msg.from_user.id)
    if status == 200:
        await state.set_state(states.Menu.main_menu)
        await main_menu_handler(msg, state)
    else:
        await state.set_state(states.Register.first_name)
        await msg.answer('Ismingizni kiriting:')


@start.message(states.Register.first_name)
async def get_first_name(msg: Message, state: FSMContext):
    context = {
        'first_name': msg.text
    }
    await state.update_data(context)
    await state.set_state(states.Register.last_name)
    await msg.answer('Familiyangizni kiriting:')


@start.message(states.Register.last_name)
async def get_last_name(msg: Message, state: FSMContext):
    context = {
        'last_name': msg.text
    }
    await state.update_data(context)
    state_data = await state.get_data()
    state_data['telegram_id'] = msg.from_user.id
    # create user
    await request.user.create(state_data)
    await state.clear()
    await start_handler(msg, state)
