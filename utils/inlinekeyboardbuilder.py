from typing import Any

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import data


def inline_keyboard_builder(template, messages: Any, call_backs: list[str], sizes: list[int], back=None,
                            back_main=None):
    builder = InlineKeyboardBuilder()
    for message, call_back in zip(messages, call_backs):
        builder.add(
            InlineKeyboardButton(
                text=message,
                callback_data=template(choice=call_back).pack()
            )
        )
    if back and back_main:
        builder.add(InlineKeyboardButton(
            text=data.back_buttons['back'],
            callback_data='back'
        ),
            InlineKeyboardButton(
                text=data.back_buttons['back_main_menu'],
                callback_data='back_main_menu'
            )
        )
    elif back:
        builder.add(InlineKeyboardButton(
            text=data.back_buttons['back'],
            callback_data='back')
        )
    builder.adjust(*sizes)
    return builder.as_markup()
