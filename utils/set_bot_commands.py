from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand


async def set_default_commands(bot):
    await bot(
        SetMyCommands(
            commands=[
                BotCommand(command='start', description='Restart qilish'),
                BotCommand(command='help', description='Xizmat haqida'),
            ]
        )
    )
