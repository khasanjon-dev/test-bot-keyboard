from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    first_name = State()
    last_name = State()


class Menu(StatesGroup):
    main_menu = State()


class CreateTest(StatesGroup):
    menu = State()
    type = State()
    mandatory_keys = State()
    first_basic_keys = State()
    second_basic_keys = State()
    science_name = State()
    science_keys = State()
    block_keys = State()


class Answer(StatesGroup):
    menu = State()
    type = State()
    science_id = State()
    block_id = State()
    science_keys = State()
    mandatory_keys = State()
    first_basic_keys = State()
    second_basic_keys = State()
