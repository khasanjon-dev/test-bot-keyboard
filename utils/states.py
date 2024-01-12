from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    first_name = State()
    last_name = State()


class Menu(StatesGroup):
    main_menu = State()
    create_test = State()


class CreateTest(StatesGroup):
    menu = State()
    type = State()
    name = State()
    keys = State()
