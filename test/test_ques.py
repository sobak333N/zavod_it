import logging
from aiogram import Bot, Dispatcher, types
# from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State , StatesGroup


API_TOKEN = '7015685401:AAFbBOl5IRl6DiEVMpseW8FVgXyIYUJpEew'

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage = storage)

# Словарь для хранения ответов пользователя
user_answers = {}


class FSMques(StatesGroup):
    name = State()
    age = State()
    city = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    await message.answer("старт!")

    # Запуск функции, которая задает первый вопрос


@dp.message_handler(commands=['new'])
async def fcm_start(message: types.Message ):


    # user_id = message.from_user.id
    await FSMques.name.set()
    await message.answer("Привет! Я буду задавать тебе несколько вопросов. Начнем?")
    await message.answer("Как тебя зовут ?")
    # Запуск функции, которая задает первый вопрос

@dp.message_handler(state=FSMques.name)
async def ask_name(message: types.Message , state: FSMContext):
    # Задаем первый вопрос
    async with state.proxy() as data:
        data['name']=message.text
    await FSMques.next()
    await message.answer("Сколько тебе лет ?")
    # Отправляем вопрос пользователю

@dp.message_handler(state=FSMques.age)
async def ask_age(message: types.Message , state: FSMContext):
    # Задаем первый вопрос
    async with state.proxy() as data:
        data['age']=message.text
    await FSMques.next()
    await message.answer("Где ты живешь")

@dp.message_handler(state=FSMques.city)
async def ask_city(message: types.Message , state: FSMContext):
    # Задаем первый вопрос
    async with state.proxy() as data:
        data['city']=message.text
    async with state.proxy() as data:
        await message.reply(str(data))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
