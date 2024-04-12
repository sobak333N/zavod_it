import logging
from aiogram import Bot, Dispatcher, types
# from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State , StatesGroup
import base64
from PIL import Image
import io
import json
# from YandexGPT_API import YandexGPTApi
# API_TOKEN = '6047293314:AAGIolk6_uOFPfSb4H1ahm-E8l8a2f-dkVk'
from create_bot import dp,bot
from memory_code_api import update
# logging.basicConfig(level=logging.INFO)

# storage = MemoryStorage()

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot,storage = storage)



class Basic(StatesGroup):
    #Базовая информация
    name = State()
    date_birth = State()
    date_death = State()
    #characteristics = State()
    author_epitaph = State()
class Info(StatesGroup):
    #Краткая информация
    place_birth = State()
    place_death = State()
    child = State()
    partner = State()
    citizenship = State()
    education = State()
    profession = State()
    awards = State()
    photo = State()
class Biography(StatesGroup):
    stage1 = State()
    stage2 = State()
    stage3 = State()



@dp.message_handler(commands=['new'])
async def fcm_start(message: types.Message ):
    await Basic.name.set()
    await message.answer("Укажите ФИО")

@dp.message_handler(state=Basic.name)
async def ask_name(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['name']=message.text
    await Basic.next()
    await message.answer("Дата рождения")

@dp.message_handler(state=Basic.date_birth)
async def ask_date_birth(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['date_birth']=message.text
    await Basic.next()
    await message.answer("Дата смерти")

@dp.message_handler(state=Basic.date_death)
async def ask_date_death(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['date_death']=message.text
    await Basic.next()
    await message.answer("Автор эпитафии")

@dp.message_handler(state=Basic.author_epitaph)
async def ask_author(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['author_epitaph']=message.text
    await state.finish()
    await Info.place_birth.set()
    await message.answer("Место рождения")

@dp.message_handler(state=Info.place_birth)
async def ask_place_birth(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['place_birth']=message.text
    await Info.next()
    await message.answer("Место смерти")

@dp.message_handler(state=Info.place_death)
async def ask_place_death(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['place_death']=message.text
    await Info.next()
    await message.answer("Дети")

@dp.message_handler(state=Info.child)
async def ask_child(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['child']=message.text
    await Info.next()
    await message.answer("Партнёр")


@dp.message_handler(state=Info.partner)
async def ask_partner(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['partner']=message.text
    await Info.next()
    await message.answer("Гражданство")

@dp.message_handler(state=Info.citizenship)
async def ask_partner(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['citizenship']=message.text
    await Info.next()
    await message.answer("Образование")

@dp.message_handler(state=Info.education)
async def ask_partner(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['education']=message.text
    await Info.next()
    await message.answer("Профессии")

@dp.message_handler(state=Info.profession)
async def ask_partner(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['profession']=message.text
    await Info.next()
    await message.answer("Награды")

@dp.message_handler(state=Info.awards)
async def ask_partner(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['awards']=message.text
    await Info.next()
    await message.answer("Скинь фото")
    


@dp.message_handler(state=Info.photo , content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message , state: FSMContext):
    # Получаем информацию о фото
    print("WTF")
    photo_info = message.photo[-1]  # Берем последнюю (самую большую) версию фото
    photo_file = await bot.get_file(photo_info.file_id)
    photo = await bot.download_file(photo_file.file_path)

    # Сохраняем фото на диск
    with open('photo.jpg', 'wb') as file:
        print("WTF2")
        file.write(photo.getvalue())

    # Конвертируем фото в base64 и добавляем в JSON
    with open('photo.jpg', 'rb') as image_file:
        print("WTF3")
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        json_data = {"url": f"data:image/png;base64,{encoded_string}"}
        json_string = json.dumps(json_data)

    # Отправляем JSON
    print("WTF4")

    
    await bot.send_message(message.chat.id, "lox")
    # print(json_string)
    async with state.proxy() as data:
        print(str(data))
        user_id = message.from_user.id
        update(user_id,data,json_string)
    await bot.send_message(message.chat.id, json_string)

    await state.finish()

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


