from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

import data
from logic.menu import main_menu_handler
from root import settings
from utils import states, request
from utils.keyboardbuilder import keyboard_builder
from utils.serializers import keys_serializer, check_answer, date_change_format

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
    status_code, science_api = await request.test.get_science(msg.text)
    if status_code == 200:
        # user avval topshirganini tekshirishim kerak
        _, user = await request.user.get(msg.from_user.id)
        status, answer_api = await request.answer.get_science({'science': msg.text, 'user': user['id']})
        if status == 404:
            await state.update_data({'science': msg.text})
            await state.set_state(states.Answer.science_keys)
            await request_science_keys(msg)
        else:
            await state.clear()
            await state.set_state(states.Menu.main_menu)
            text = (f"❇️ Siz bu testga avvalroq qatnashgansiz !\n\n"
                    f"🆔 Test id:"
                    f"<blockquote>{answer_api['science']}</blockquote>\n"
                    f"📚 Savollar soni:"
                    f"<blockquote>{answer_api['size']}</blockquote>\n"
                    f"✅ To'g'ri javoblar soni:"
                    f"<blockquote>{answer_api['score']}</blockquote>\n"
                    f"⏰ Siz topshirgan vaqt:"
                    f"<blockquote>{date_change_format(answer_api['created_at'])}</blockquote>\n"
                    f"〽️ Natija:"
                    f"<blockquote>{(answer_api['score'] / answer_api['size'] * 100):.2f} %</blockquote>\n\n"
                    f"❗️ Noto'g'ri javoblaringiz test yakunlanganidan so'ng yuboriladi!\n")
            markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
            await msg.answer(text, ParseMode.HTML, reply_markup=markup)
    else:
        text = ('⚠️ Bunday Test mavjud emas\n'
                '♻️ Test 🆔 tekshirib qayta yuboring')
        await state.set_state(states.Answer.science_id)
        await msg.answer(text)


# request science keys
async def request_science_keys(msg: Message):
    text = ("Test javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await msg.answer("⚠️ Siz bir marta tekshirish huquqiga egasiz e'tiborli bo'ling!")
    await msg.answer(text, ParseMode.HTML)


# get science keys
@answer.message(states.Answer.science_keys)
async def get_science_keys(msg: Message, state: FSMContext):
    get_data = await state.get_data()
    _, test = await request.test.get_science(get_data['science'])
    keys_api = test['keys']
    keys = await keys_serializer(msg.text)
    if len(keys) != len(keys_api):
        text = (f"Savollar soni: <b>{len(keys_api)}</b> ta\n"
                f"Siz yuborgan kalitlar soni <b>{len(keys)}</b> ta\n"
                f"Kalitlaringizni tekshirib qayta kiriting ⚠️")
        await msg.answer(text, ParseMode.HTML)
    else:
        _, user = await request.user.get(msg.from_user.id)
        true_answers, false_keys = await check_answer(keys, keys_api)
        get_data['user'] = user['id']
        get_data['false_keys'] = false_keys
        await science_result(msg, state, get_data)


async def science_result(msg: Message, state: FSMContext, get_data: dict):
    status, answer_api = await request.answer.create_science(get_data)
    if status == 201:
        _, user = await request.user.get(msg.from_user.id)
        text = (f"👤 Foydalanuvchi:\n"
                f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>\n\n"
                f"🆔 Test id:"
                f"<blockquote>{answer_api['science']}</blockquote>\n"
                f"📚 Savollar soni:"
                f"<blockquote>{answer_api['size']}</blockquote>\n"
                f"✅ To'g'ri javoblar soni:"
                f"<blockquote>{answer_api['score']}</blockquote>\n"
                f"⏰ Siz topshirgan vaqt:"
                f"<blockquote>{date_change_format(answer_api['created_at'])}</blockquote>\n"
                f"〽️ Natija:"
                f"<blockquote>{(answer_api['score'] / answer_api['size'] * 100):.2f} %</blockquote>\n\n"
                f"❗️ Noto'g'ri javoblaringiz test yakunlanganidan so'ng yuboriladi!\n")
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


# ============================================================================================================
#    B L O C K
# ============================================================================================================


# request block id
async def request_block_id(msg: Message, state: FSMContext):
    await state.set_state(states.Answer.block_id)
    await msg.answer('Test 🆔 ni yuboring:', reply_markup=ReplyKeyboardRemove())


# get block id
@answer.message(states.Answer.block_id)
async def get_block_id(msg: Message, state: FSMContext):
    # check available test id
    status_code, block_api = await request.test.get_block(msg.text)
    if status_code == 200:
        # user avval topshirganini tekshirishim kerak
        _, user = await request.user.get(msg.from_user.id)
        context = {
            'user': user['id'],
            'block': msg.text
        }
        status, answer_api = await request.answer.get_block(context)
        if status == 404:
            await state.update_data({'block': msg.text})
            await state.set_state(states.Answer.mandatory_keys)
            await request_mandatory_keys(msg)
        else:
            await state.clear()
            await state.set_state(states.Menu.main_menu)
            # TODO ozgina chala joyi bor

            text = (f"❇️ Siz bu testga avvalroq qatnashgansiz !\n\n"
                    f"🆔 Test id:"
                    f"<blockquote>{answer_api['block']}</blockquote>\n"
                    f"📚 Savollar soni:"
                    f"<blockquote>90</blockquote>\n"
                    f"✅ To'g'ri javoblar soni:"
                    f"<blockquote>{len(answer_api['true_answers'])}</blockquote>\n"
                    f"⏰ Siz topshirgan vaqt:"
                    f"<blockquote>{date_change_format(answer_api['created_at'])}</blockquote>\n"
                    f"〽️ Natija:"
                    f"<blockquote>{(len(answer_api['true_answers']) / answer_api['size'] * 100):.2f} %</blockquote>\n\n"
                    f"❗️ Noto'g'ri javoblaringiz test yakunlanganidan so'ng yuboriladi!\n")
            markup = keyboard_builder(data.main_menu.values(), [1, 1, 2])
            await msg.answer(text, ParseMode.HTML, reply_markup=markup)

    else:
        text = ('⚠️ Bunday Test mavjud emas\n'
                '♻️ Test 🆔 tekshirib qayta yuboring')
        await state.set_state(states.Answer.science_id)
        await msg.answer(text)


# request mandatory keys
async def request_mandatory_keys(msg: Message):
    text = ("Majburiy fan javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await msg.answer("⚠️ Siz bir marta tekshirish huquqiga egasiz e'tiborli bo'ling!")
    await msg.answer(text, ParseMode.HTML)


# get mandatory keys
@answer.message(states.Answer.mandatory_keys)
async def get_mandatory_keys(msg: Message, state: FSMContext):
    keys = await keys_serializer(msg.text)
    if len(keys) != 30:
        text = (f"Siz yuborgan kalitlar soni <b>{len(keys)}</b> ta\n"
                f"Majburiy fan savollar soni: <b>30</b> ta\n"
                f"Kalitlaringizni tekshirib qayta kiriting ⚠️")
        await msg.answer(text, ParseMode.HTML)
    else:
        await state.update_data({'mandatory_keys': msg.text})
        await state.set_state(states.Answer.first_basic_keys)
        await request_first_basic_keys(msg)


# request first basic keys
async def request_first_basic_keys(msg: Message):
    text = ("1-asosiy fan javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await msg.answer(text, ParseMode.HTML)


# get first basic keys
@answer.message(states.Answer.first_basic_keys)
async def get_first_basic_keys(msg: Message, state: FSMContext):
    keys = await keys_serializer(msg.text)
    if len(keys) != 30:
        text = (f"Siz yuborgan kalitlar soni <b>{len(keys)}</b> ta\n"
                f"1-asosiy fan savollar soni: <b>30</b> ta\n"
                f"Kalitlaringizni tekshirib qayta kiriting ⚠️")
        await msg.answer(text, ParseMode.HTML)
    else:
        await state.update_data({'first_basic_keys': msg.text})
        await state.set_state(states.Answer.second_basic_keys)
        await request_second_basic_keys(msg)


# request second basic keys
async def request_second_basic_keys(msg: Message):
    text = ("2-asosiy fan javoblarini quyidagi ko'rinishda kiriting:\n\n"
            "1-usul:    <b>abcdabcd.....abc</b>\n\n"
            "2-usul:    <b>1a2b3c4d5a6b....29a30b</b>")
    await msg.answer(text, ParseMode.HTML)


# get second basic keys
@answer.message(states.Answer.second_basic_keys)
async def get_second_basic_keys(msg: Message, state: FSMContext):
    keys = await keys_serializer(msg.text)
    if len(keys) != 30:
        text = (f"Siz yuborgan kalitlar soni <b>{len(keys)}</b> ta\n"
                f"2-asosiy fan savollar soni: <b>30</b> ta\n"
                f"Kalitlaringizni tekshirib qayta kiriting ⚠️")
        await msg.answer(text, ParseMode.HTML)
    else:
        get_data = await state.get_data()
        _, user = await request.user.get(msg.from_user.id)
        status, test = await request.test.get_block(get_data['block'])
        keys_api = test['keys']
        true_answers, false_answers = await check_answer(keys, keys_api)
        get_data['user'] = user['id']
        get_data['true_answers'] = true_answers
        get_data['false_answers'] = false_answers
        await block_result(msg, state, get_data)


async def block_result(msg: Message, state: FSMContext, get_data: dict):
    status, answer_api = await request.answer.create_block(get_data)
    if status == 201:
        _, user = await request.user.get(msg.from_user.id)
        text = (f"👤 Foydalanuvchi:\n"
                f"<a href='tg://user?id={user['telegram_id']}'>{user['first_name']} {user['last_name']}</a>\n\n"
                f"🆔 Test id:"
                f"<blockquote>{answer_api['block']}</blockquote>\n"
                f"📚 Savollar soni:"
                f"<blockquote>{answer_api['size']}</blockquote>\n"
                f"✅ To'g'ri javoblar soni:"
                f"<blockquote>{len(answer_api['true_answers'])}</blockquote>\n"
                f"⏰ Siz topshirgan vaqt:"
                f"<blockquote>{date_change_format(answer_api['created_at'])}</blockquote>\n"
                f"〽️ Natija:"
                f"<blockquote>{(len(answer_api['true_answers']) / answer_api['size'] * 100):.2f} %</blockquote>\n\n"
                f"❗️ Noto'g'ri javoblaringiz test yakunlanganidan so'ng yuboriladi!\n")
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
# TODO need fix return result
