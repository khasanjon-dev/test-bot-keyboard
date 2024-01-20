from aiogram import F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from data import data
from logic.menu import main_menu_handler
from utils import states, requests, keys_serializer
from utils.keyboardbuilder import keyboard_builder

create_test = Router()


# show create test menu
@create_test.message(F.text == data.main_menu['create_test'], states.Menu.main_menu)
@create_test.message(states.CreateTest.menu)
async def create_test_menu(msg: Message, state: FSMContext):
    markup = keyboard_builder(data.create_test_menu.values(), [2], True)
    await state.set_state(states.CreateTest.type)
    await msg.answer('Test turini tanlang:', reply_markup=markup)


# get test type
@create_test.message(states.CreateTest.type)
async def get_test_type(msg: Message, state: FSMContext):
    if msg.text == data.create_test_menu['science']:
        context = {
            'type': 'science'
        }
        await state.update_data(context)
        await request_science_name(msg, state)
    elif msg.text == data.create_test_menu['block']:
        context = {
            'test_type': 'block'
        }
        await state.update_data(context)
        await block_test_enter_example(msg, state)
    elif msg.text == data.back_buttons['back']:
        await state.set_state(states.Menu.main_menu)
        await main_menu_handler(msg, state)
    else:
        await state.set_state(states.CreateTest.menu)
        await create_test_menu(msg, state)


# request test name for input
async def request_science_name(msg: Message, state: FSMContext):
    await state.set_state(states.CreateTest.science_name)
    await msg.answer('Fan nomini kiriting:', reply_markup=ReplyKeyboardRemove())


# get science test name and return example test enter keys
@create_test.message(states.CreateTest.science_name)
async def get_science_name(msg: Message, state: FSMContext):
    await state.update_data({'name': msg.text})
    await state.set_state(states.CreateTest.science_keys)
    text = ("Test javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await msg.answer(text, ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


# example to enter test answers for Block Test
async def block_test_enter_example(msg: Message, state: FSMContext):
    text = ("Test javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....89a90b</b>")
    await state.set_state(states.CreateTest.block_keys)
    await msg.answer(text, ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


# get block test keys
@create_test.message(states.CreateTest.block_keys)
async def get_block_test_keys(msg: Message, state: FSMContext):
    await state.update_data({'keys': msg.text})
    get_data = await state.get_data()
    status_code, user = await requests.get_user(msg.from_user.id)
    get_data['id'] = user['id']
    get_data['size'] = len(keys_serializer(get_data['keys']))
    test = await requests.create_block_test(get_data)
    await test_final_response(msg, state, test, user)


# get test keys and return test id
@create_test.message(states.CreateTest.science_keys)
async def get_test_keys(msg: Message, state: FSMContext):
    await state.update_data({'keys': msg.text})
    get_data = await state.get_data()
    status_code, user = await requests.get_user(msg.from_user.id)
    get_data['id'] = user['id']
    get_data['size'] = len(keys_serializer(get_data['keys']))
    test = await requests.create_test(get_data)
    await test_final_response(msg, state, test, user)


# return finally test response
async def test_final_response(msg: Message, state: FSMContext, test, user):
    await msg.answer(f"Test yaratildi!\n"
                     f"Test id orqali javoblarni tekshirish mumkin .")
    text = (f"🆔 Test id:\n"
            f"<pre>{test['id']}</pre>\n"
            f"✉️ Savollar soni:\n"
            f"<pre>{test['size']}</pre>\n"
            f"✍️ Test muallifi:\n"
            f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>")
    markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
    await msg.answer(text, ParseMode.HTML, reply_markup=markup)
    await state.clear()
    await state.set_state(states.Menu.main_menu)
