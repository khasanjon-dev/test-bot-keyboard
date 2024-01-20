from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

import data
from logic.menu import main_menu_handler
from utils import states
from utils.keyboardbuilder import keyboard_builder

check_answer = Router()


@check_answer.message(F.text == data.main_menu['check_answer'], states.Menu.main_menu)
@check_answer.message(states.CheckAnswer.menu)
async def check_answer_menu(msg: Message, state: FSMContext):
    markup = keyboard_builder(data.create_test_menu.values(), [2], True)
    await state.set_state(states.CheckAnswer.type)
    await msg.answer('Test turini tanlang:', reply_markup=markup)


@check_answer.message(states.CheckAnswer.type)
async def get_test_type(msg: Message, state: FSMContext):
    if msg.text == data.create_test_menu['science']:
        context = {
            'type': 'science'
        }
        await state.update_data(context)
        await state.set_state(states.CheckAnswer.id)
        await request_test_id(msg, state)
    elif msg.text == data.create_test_menu['block']:
        context = {
            'type': 'block'
        }
        await state.update_data(context)
        await state.set_state(states.CheckAnswer.id)
        await request_test_id(msg, state)
    elif msg.text == data.back_buttons['back']:
        await state.set_state(states.Menu.main_menu)
        await main_menu_handler(msg, state)
    else:
        await state.set_state(states.CreateTest.menu)
        await check_answer_menu(msg, state)


# request test ID
@check_answer.message(F.text == data.main_menu['check_answer'], states.Menu.main_menu)
async def request_test_id(msg: Message, state: FSMContext):
    await state.set_state(states.CheckAnswer.id)
    await msg.answer("Test 🆔 ni yuboring:", reply_markup=ReplyKeyboardRemove())


# get test ID and request test keys
@check_answer.message(states.CheckAnswer.id)
async def get_test_id(msg: Message, state: FSMContext):
    context = {
        'test_id': msg.text,
    }
    await state.set_data(context)
    text = ("Test javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....89a90b</b>")
    await state.set_state(states.CheckAnswer.keys)
    await msg.answer(text, ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    await msg.answer("Siz bir marta tekshirish huquqiga egasiz e'tiborli bo'ling!")


@check_answer.message(states.CheckAnswer.keys)
async def get_test_keys(msg: Message, state: FSMContext):
    pass
