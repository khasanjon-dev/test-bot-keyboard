from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data import data


def keyboard_builder(messages: list, sizes: list | None = None, back=False, main=False):
    builder = ReplyKeyboardBuilder()
    for message in messages:
        builder.add(
            KeyboardButton(text=message)
        )
    if back:
        builder.add(
            KeyboardButton(text=data.back_buttons['back'])
        )
    if main:
        builder.add(
            KeyboardButton(text=data.back_buttons['back_main_menu'])
        )
    builder.adjust(*sizes)
    return builder.as_markup(resize_keyboard=True)
