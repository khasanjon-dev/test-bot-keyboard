from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.requests import get_user

start = Router()


@start.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()
    status, data = await get_user(msg.from_user.id)
    if status == 200:
        pass
    else:
