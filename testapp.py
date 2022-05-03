import glob
import tabula
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from src.machine import Meta
from src.config import TOKEN
from src import buttons
p1 = Meta()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    
    await message.reply("Привет!\nНапиши класс и букву слитно *8Б*!")

@dp.message_handler()
async def catch_message(msg: types.Message):
    await p1.state_machine(msg)

    
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)