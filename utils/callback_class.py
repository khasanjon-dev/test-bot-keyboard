from enum import Enum

from aiogram.filters.callback_data import CallbackData


class BackMenu(str, Enum):
    back = 'back'
    back_main_menu = 'back_main_menu'
    none = 'none'


class BackMenuCallback(CallbackData, prefix='back'):
    choice: BackMenu


class MainMenu(str, Enum):
    create_test = 'create_test'
    check_answer = 'check_answer'
    about = 'about'
    about_me = 'about_me'


class MainMenuCallback(CallbackData, prefix='main_menu'):
    choice: MainMenu


class CreateTest(str, Enum):
    block_test = 'block'
    science_test = 'science'
    back = 'back'


class CreateTestCallback(CallbackData, prefix='test'):
    choice: CreateTest


class CreateTestCheck(str, Enum):
    confirm = 'confirm'
    re_create = 're_create'
    back_main_menu = 'back_main_menu'


class CreateTestCheckCallback(CallbackData, prefix='check'):
    choice: CreateTestCheck
