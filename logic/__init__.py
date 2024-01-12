"""This package is used for a bot logic implementation."""
from logic.create_test import create_test
from logic.menu import menu
from logic.start import start

routers = (start, menu, create_test)
