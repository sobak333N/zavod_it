import logging
from aiogram import Bot, Dispatcher, types
# from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State , StatesGroup
# from YandexGPT_API import YandexGPTApi
# API_TOKEN = '6047293314:AAGIolk6_uOFPfSb4H1ahm-E8l8a2f-dkVk'
from create_bot import dp,bot
# logging.basicConfig(level=logging.INFO)

# storage = MemoryStorage()

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot,storage = storage)



class FSMques(StatesGroup):
    name = State()
    age = State()
    city = State()
    ans = State()





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
    
    # gpt = YandexGPTApi(config="config.ini")
    # prompt = [{
    #     "role": "user",
    #     "text": f"Напиши биографию {data['name']}. Возраст: {data['age']}. Город проживания: {data['city']}. При выводе не пиши специальные специальные символы \n и отчёты о работе вывода"}]

    # response = gpt.make_request(prompt)
    #result=response.json()['result']['alternatives'][0]['message']['text']
    # await message.answer(response)




def register_handlers_ques(dp : Dispatcher):
    dp.register_message_handler(fcm_start , commands=['new'])
    dp.register_message_handler(ask_name)
    dp.register_message_handler(ask_age)
    dp.register_message_handler(ask_city)


