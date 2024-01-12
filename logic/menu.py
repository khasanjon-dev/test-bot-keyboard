from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data import data
from utils import states
from utils.keyboardbuilder import keyboard_builder

menu = Router()


@menu.message(states.Menu.main_menu)
async def main_menu_handler(msg: Message):
    markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
    await msg.answer("Kerakli bo'limlardan birini tanlang!", reply_markup=markup)
