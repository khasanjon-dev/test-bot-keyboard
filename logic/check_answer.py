from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

import data
from logic.menu import main_menu_handler
from root import settings
from utils import states, request, keys_serializer, check_answer
from utils.keyboardbuilder import keyboard_builder

answer = Router()


@answer.message(F.text == data.main_menu['check_answer'], states.Menu.main_menu)
@answer.message(states.Answer.menu)
async def check_answer_menu(msg: Message, state: FSMContext):
    markup = keyboard_builder(data.create_test_menu.values(), [2], True)
    await state.set_state(states.Answer.type)
    await msg.answer('Test turini tanlang:', reply_markup=markup)


@answer.message(states.Answer.type)
async def get_test_type(msg: Message, state: FSMContext):
    if msg.text == data.create_test_menu['science']:
        context = {
            'type': 'science'
        }
        await state.update_data(context)
        await state.set_state(states.Answer.science_id)
        await request_science_id(msg, state)
    elif msg.text == data.create_test_menu['block']:
        context = {
            'type': 'block'
        }
        await state.update_data(context)
        await state.set_state(states.Answer.block_id)
        # await request_test_id(msg, state)
    elif msg.text == data.back_buttons['back']:
        await state.set_state(states.Menu.main_menu)
        await main_menu_handler(msg, state)
    else:
        await state.set_state(states.Answer.menu)
        await check_answer_menu(msg, state)


# ============================================================================================================
#    S C I E N C E
# ============================================================================================================

# request science id
async def request_science_id(msg: Message, state: FSMContext):
    await state.set_state(states.Answer.science_id)
    await msg.answer("Test 🆔 ni yuboring:", reply_markup=ReplyKeyboardRemove())


# get science id
@answer.message(states.Answer.science_id)
async def get_science_id(msg: Message, state: FSMContext):
    # check available this test id
    status_code, science_api = await request.science.get(msg.text)
    if status_code == 200:
        # user avval topshirganini tekshirishim kerak
        _, user = await request.user.get(msg.from_user.id)
        status, answer_api = await request.answer.get({'test': msg.text, 'user': user['id']})
        if status == 404:
            await state.update_data({'test': msg.text})
            await state.set_state(states.Answer.science_keys)
            await request_science_keys(msg)
        else:
            await state.clear()
            await state.set_state(states.Menu.main_menu)
            text = (f"❇️ Siz bu testga avvalroq qatnashgansiz !\n\n"
                    f"🆔 Test id:\n"
                    f"<blockquote>{science_api['id']}</blockquote>\n"
                    f"✉️ Savollar soni:\n"
                    f"<blockquote>{science_api['size']}</blockquote>\n"
                    f"✅ To'g'ri javoblar soni:\n"
                    f"<blockquote>{answer_api['true_answers']}</blockquote>\n"
                    f"〽️ Natija:"
                    f"<blockquote>{(answer_api['true_answers'] / science_api['size'] * 100):.2f} %</blockquote>")
            markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
            await msg.answer(text, ParseMode.HTML, reply_markup=markup)
    else:
        text = ('⚠️ Bunday Test mavjud emas\n'
                '🆔♻️ Test id tekshirib qayta yuboring')
        await state.set_state(states.Answer.science_id)
        await msg.answer(text)


# request science keys
async def request_science_keys(msg: Message):
    text = ("Test javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....89a90b</b>")
    await msg.answer("⚠️ Siz bir marta tekshirish huquqiga egasiz e'tiborli bo'ling!")
    await msg.answer(text, ParseMode.HTML)


# get science keys
@answer.message(states.Answer.science_keys)
async def get_science_keys(msg: Message, state: FSMContext):
    get_data = await state.get_data()
    _, test = await request.science.get(get_data['test'])
    keys_api = keys_serializer(test['keys'])
    keys = keys_serializer(msg.text)
    if len(keys) != len(keys_api):
        text = (f"Savollar soni: <b>{len(keys_api)}</b>\n"
                f"Siz yuborgan kalitlar soni <b>{len(keys)}</b>\n"
                f"Kalitlaringizni tekshirib qayta kiriting ⚠️")
        await msg.answer(text, ParseMode.HTML)
    else:
        _, user = await request.user.get(msg.from_user.id)
        true_answers, false_answers = await check_answer(keys, keys_api)
        get_data['keys'] = keys
        get_data['user'] = user['id']
        get_data['true_answers'] = true_answers
        get_data['false_answers'] = false_answers
        await science_result(msg, state, get_data)


'''
👤 Foydalanuvchi: 
Aliyev Vali

📖 Test kodi: 93630
✏️ Jami savollar soni: 8 ta
✅ To'g'ri javoblar soni: 8 ta
🔣 Foiz : 100 %



☝️ Noto`g`ri javoblaringiz test yakunlangandan so'ng yuboriladi.
--------------------------------
🕐 Sana, vaqt: 2024-01-19 17:14:30
'''


async def science_result(msg: Message, state: FSMContext, get_data: dict):
    status, answer_api = await request.answer.create(get_data)
    if status == 201:
        _, user = await request.user.get(msg.from_user.id)
        text = (f"👤 Foydalanuvchi:\n"
                f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>\n\n"
                f"🆔 Test id:\n"
                f"<blockquote>{answer_api['test']}</blockquote>\n"
                f"✉️ Savollar soni:\n"
                f"<blockquote>{answer_api['true_answers'] + answer_api['false_answers']}</blockquote>\n"
                f"✅ To'g'ri javoblar soni:\n"
                f"<blockquote>{answer_api['true_answers']}</blockquote>\n"
                f"〽️ Natija:"
                f"<blockquote>{(answer_api['true_answers'] / (answer_api['true_answers'] + answer_api['false_answers']) * 100):.2f} %</blockquote>")
        markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
        await state.clear()
        await state.set_state(states.Menu.main_menu)
        await msg.answer(text, ParseMode.HTML, reply_markup=markup)
    else:
        markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
        await msg.answer(f"⚠️ Xatolik aniqlandi\n"
                         f"Iltimos adminga murojat qiling!\n"
                         f"✍️ {settings.admin_username}", reply_markup=markup)
        await state.clear()
        await state.set_state(states.Menu.main_menu)
