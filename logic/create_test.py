from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from data import data
from utils import states, requests, keys_serializer
from utils.keyboardbuilder import keyboard_builder

create_test = Router()


@create_test.message(states.CreateTest.menu)
async def create_test_menu_handler(msg: Message, state: FSMContext):
    markup = keyboard_builder(data.create_test_menu.values(), [2])
    await state.set_state(states.CreateTest.type)
    await msg.answer('Kerakli test turini tanlang:', reply_markup=markup)


@create_test.message(states.CreateTest.type)
async def get_test_type(msg: Message, state: FSMContext):
    if msg.text == data.create_test_menu['science']:
        context = {
            'type': 'science'
        }
        await state.update_data(context)
        await state.set_state(states.CreateTest.name)
        await msg.answer('Fan nomini kiriting:', reply_markup=ReplyKeyboardRemove())
    elif msg.text == data.create_test_menu['block']:
        context = {
            'test_type': 'block'
        }
        await state.update_data(context)


# get test name and return example test enter keys
@create_test.message(states.CreateTest.name)
async def get_test_name(msg: Message, state: FSMContext):
    await state.update_data({'name': msg.text})
    await state.set_state(states.CreateTest.keys)
    text = ("Test javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await msg.answer(text, ParseMode.HTML)


# get test keys and return test id
@create_test.message(states.CreateTest.keys)
async def get_test_keys(msg: Message, state: FSMContext):
    await state.update_data({'keys': msg.text})
    get_data = await state.get_data()
    status_code, user = await requests.get_user(msg.from_user.id)
    get_data['telegram_id'] = msg.from_user.id
    get_data['id'] = user['id']
    test = await requests.create_test(get_data)
    await msg.answer(f"Test yaratildi!\n"
                     f"test id orqali javoblarni tekshirish mumkin .")
    text = (f"🆔 Test id:\n"
            f"<pre>{test['id']}</pre>\n"
            f"📦 Savollar soni:\n"
            f"<pre>{len(keys_serializer(test['keys']))}</pre>\n"
            f"✍️ Test muallifi:\n"
            f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>")
    await msg.answer(text, ParseMode.HTML)
    await state.clear()
