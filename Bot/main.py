from asyncio import Lock

from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
import config
from sql import create_adres_data,edit_adres_data,db_start
# ,receiving_adres_data

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# async def on_startup():
#     on_startup = on_startup()

lock = Lock()

class RegisterMessages(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()

class DB:
    answer_data = {}

@dp.message_handler(commands='start', state=None)
async def start(message: types.Message):
    await RegisterMessages.step1.set()
    await bot.send_message(message.from_user.id, text='Здравствуйте!  Введите имя:',)
    await db_start(message.from_user.id)
    await create_adres_data(message.from_user.id)

# @dp.message_handler(commands='text', state=None)
# async def eg_step(message: types.Message):
#     await RegisterMessages.step2.set()
#     await create_adres_data(user = message.from_user.id)
#     await bot.send_message(message.from_user.id, text='Здравствуйте!  Введите имя:')


@dp.message_handler(content_types='text', state=RegisterMessages.step1)
async def reg_step2(message: types.Message):
    async with lock:
        DB.answer_data['name'] = message.text
    await bot.send_message(message.from_user.id, text='Принято! Введите отчество:')
    await RegisterMessages.next()

@dp.message_handler(content_types='text', state=RegisterMessages.step2)
async def reg_step3(message: types.Message):
    async with lock:
        DB.answer_data['surname'] = message.text
    await bot.send_message(message.from_user.id, text='Принято! Введите номер квартиры:')
    await RegisterMessages.next()

@dp.message_handler(content_types='text', state=RegisterMessages.step3)
async def reg_step4(message: types.Message):
    async with lock:
        DB.answer_data['ap_number'] = message.text
    await bot.send_message(message.from_user.id, text='Принято! Введите номер телефона:')
    await RegisterMessages.next()

@dp.message_handler(content_types='text', state=RegisterMessages.step4)
async def reg_step5(message: types.Message, state: FSMContext):
    async with lock:
        DB.answer_data['phone'] = message.text
    await bot.send_message(message.from_user.id, text='Принято!  Чтобы посмотреть данные введите команду /check',)
  
    await state.finish()

@dp.message_handler(commands='check')
async def get_reg_data(message: types.Message):
    answer = ''
    answer += f'Имя: {DB.answer_data["name"]}\n\n'
    answer += f'Отчество: {DB.answer_data["surname"]}\n\n'
    answer += f'Номер квартиры: {DB.answer_data["ap_number"]}\n\n'
    answer += f'Номер телефона: {DB.answer_data["phone"]}'

    
    await bot.send_message(message.from_user.id, text=answer)
    await edit_adres_data(message.from_user.id)

if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
          skip_updates=True,
          
          )

