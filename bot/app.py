# данный файл = точка входа в приложение
import asyncio
import logging
from handlers import molecule, some_operation
from aiogram import Bot, Dispatcher, types
from private import TOKEN
from aiogram.types import BotCommand
from keyboards.set_menu import default_commands


# логирование
logging.basicConfig(level=logging.INFO)
# объект бота
bot = Bot(token=TOKEN)

# Диспетчер
# Диспетчер — объект, занимающийся получением апдейтов от Telegram
# с последующим выбором хэндлера для обработки принятого апдейта.
dp = Dispatcher()
dp.include_router(molecule.router)


dp.startup.register(default_commands)
dp.run_polling(bot)


# Запуск процесса поллинга новых апдейтов
# определяем асинхронную функцию
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())