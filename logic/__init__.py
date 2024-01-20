"""This package is used for a bot logic implementation."""
from logic.check_answer import check_answer
from logic.create_test import create_test
from logic.menu import menu
from logic.start import start

routers = (start, create_test, check_answer, menu)
