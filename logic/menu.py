from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data import data
from logic.create_test import create_test_menu_handler
from utils import states
from utils.keyboardbuilder import keyboard_builder

menu = Router()


@menu.message(states.Menu.main_menu)
async def main_menu_handler(msg: Message, state: FSMContext):
    if msg.text == data.main_menu['create_test']:
        await state.set_state(states.CreateTest.menu)
        await create_test_menu_handler(msg, state)
    else:
        markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
        await msg.answer("Kerakli bo'limlardan birini tanlang!", reply_markup=markup)
