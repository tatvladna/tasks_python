from aiogram import Bot
from aiogram.types import BotCommand

async def default_commands(bot: Bot):
    menu_commands = [
        BotCommand(command="/search", description="Search molecule"),
        BotCommand(command="/start", description="Start bot"),
        BotCommand(command="/cancel", description="Cancel running task"),
        BotCommand(command="/help", description="Manual")
    ]

    await bot.set_my_commands(menu_commands)
