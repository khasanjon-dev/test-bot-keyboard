from aiogram import F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from data import data
from logic.menu import main_menu_handler
from root import settings
from utils import states, request
from utils.keyboardbuilder import keyboard_builder
from utils.serializers import keys_serializer

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
        await request_mandatory(msg, state)
    elif msg.text == data.back_buttons['back']:
        await state.set_state(states.Menu.main_menu)
        await main_menu_handler(msg, state)
    else:
        await state.set_state(states.CreateTest.menu)
        await create_test_menu(msg, state)


# =====================================================================================================================
#           S C I E N C E
# =====================================================================================================================


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


# get test keys and return test id
@create_test.message(states.CreateTest.science_keys)
async def get_science_test_keys(msg: Message, state: FSMContext):
    await state.update_data({'keys': msg.text})
    get_data = await state.get_data()
    status_code, user = await request.user.get(msg.from_user.id)
    get_data['id'] = user['id']
    get_data['keys'] = await keys_serializer(get_data['keys'], True)
    test = await request.science.create(get_data)
    await since_test_final_response(msg, state, test, user)


# return finally test response
async def since_test_final_response(msg: Message, state: FSMContext, test, user):
    await msg.answer(f"Test yaratildi ✅")
    text = (f"🆔 Test id:\n"
            f"<blockquote>{test['id']}</blockquote>\n"
            f"✉️ Savollar soni:\n"
            f"<blockquote>{test['size']}</blockquote>\n"
            f"✍️ Test muallifi:\n"
            f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>\n\n"
            f"<b>♻️ Test ID orqali javoblarni tekshirish mumkin</b>")
    markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
    await state.clear()
    await state.set_state(states.Menu.main_menu)
    await msg.answer(text, ParseMode.HTML, reply_markup=markup)


# =====================================================================================================================
#           B L O C K
# =====================================================================================================================


# request mandatory
async def request_mandatory(msg: Message, state: FSMContext):
    text = ("<b>Majburiy fanlar kalitlarini kiriting: </b>\n\n"
            "Kalitlar quyidagi ko'rinishlarda kiritilishi mumkin:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await state.set_state(states.CreateTest.mandatory_keys)
    await msg.answer(text, ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    text = ("<b>Bunda kalitlar quyidagicha qabul qilinadi:</b>\n\n"
            "<b>1-10</b> kalitlar <u>Ona tili</u>\n"
            "<b>11-20</b> kalitlar <u>Matematika</u>\n"
            "<b>21-30</b> kalitlar <u>Tarix</u>")
    await msg.answer(text, ParseMode.HTML)


# get mandatory  keys
@create_test.message(states.CreateTest.mandatory_keys)
async def get_mandatory_keys(msg: Message, state: FSMContext):
    keys = await keys_serializer(msg.text)
    if len(keys) != 30:
        await msg.answer("⚠️ Siz kiritgan kalitlar soni 30 ta emas\n"
                         "Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data({'mandatory_keys': msg.text})
        await request_first_basic_keys(msg, state)


# request first basic keys
async def request_first_basic_keys(msg: Message, state: FSMContext):
    text = ("<b>1-asosiy fan kalitlarini kiriting:</b>\n\n"
            "Kalitlar quyidagi ko'rinishlarda kiritilishi mumkin:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>31a32b33c34d35a36b....59a60b</b>")
    await state.set_state(states.CreateTest.first_basic_keys)
    await msg.answer(text, ParseMode.HTML)


# get first basic keys
@create_test.message(states.CreateTest.first_basic_keys)
async def get_first_basic_keys(msg: Message, state: FSMContext):
    keys = await keys_serializer(msg.text)
    if len(keys) != 30:
        await msg.answer("⚠️ Siz kiritgan kalitlar soni 30 ta emas\n"
                         "Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data({'first_basic_keys': msg.text})
        await request_second_basic_keys(msg, state)


# request second basic keys
async def request_second_basic_keys(msg: Message, state: FSMContext):
    text = ("<b>2-asosiy fan kalitlarini kiriting:</b>\n\n"
            "Kalitlar quyidagi ko'rinishlarda kiritilishi mumkin:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>61a62b63c64d65a66b....89a90b</b>")
    await state.set_state(states.CreateTest.second_basic_keys)
    await msg.answer(text, ParseMode.HTML)


# get second basic keys
@create_test.message(states.CreateTest.second_basic_keys)
async def get_second_basic_keys(msg: Message, state: FSMContext):
    keys = await keys_serializer(msg.text)
    if len(keys) != 30:
        await msg.answer("⚠️ Siz kiritgan kalitlar soni 30 ta emas\n"
                         "Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data({'second_basic_keys': msg.text})
        await save_block_test(msg, state)


# save block test
async def save_block_test(msg: Message, state: FSMContext):
    get_data = await state.get_data()
    _, user = await request.user.get(msg.from_user.id)
    get_data['author'] = user['id']
    keys = get_data['mandatory_keys'] + get_data['first_basic_keys'] + get_data['second_basic_keys']
    get_data['keys'] = await keys_serializer(keys, True)
    status, block = await request.block.create(get_data)
    if status == 201:
        await block_test_final_response(msg, state, block, user)
    else:
        markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
        await msg.answer(f"⚠️ Xatolik aniqlandi\n"
                         f"Iltimos adminga murojat qiling!\n"
                         f"✍️ {settings.admin_username}", reply_markup=markup)
        await state.clear()
        await state.set_state(states.Menu.main_menu)


# return finally test response
async def block_test_final_response(msg: Message, state: FSMContext, test, user):
    await msg.answer(f"Blok Test yaratildi ✅")
    text = (f"🆔 Test id:\n"
            f"<blockquote>{test['id']}</blockquote>\n"
            f"✉️ Savollar soni:\n"
            f"<blockquote>{test['size']}</blockquote>\n"
            f"✍️ Test muallifi:\n"
            f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>\n\n"
            f"<b>♻️ Test ID orqali javoblarni tekshirish mumkin</b>")
    markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
    await state.clear()
    await state.set_state(states.Menu.main_menu)
    await msg.answer(text, ParseMode.HTML, reply_markup=markup)
