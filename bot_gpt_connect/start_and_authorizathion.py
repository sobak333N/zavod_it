from aiogram import Dispatcher, types
from create_bot import dp,bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State , StatesGroup
from memory_code_api import auth

import requests
import json

# auth = False
# button_text = "Нажми меня"
# keyboard.add(button_text)


class FSMauth(StatesGroup):
    login = State()
    passw = State()

class Form(StatesGroup):
    waiting_for_action = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    await message.answer("старт!")
    # if auth:
    #     pass
    # else:
    await Form.waiting_for_action.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    button_text = "auth"
    keyboard.add(button_text)
    await message.answer("Привет! Нажми кнопку.", reply_markup=keyboard)
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.add(types.KeyboardButton(text="Зарегистрироваться", request_contact=True))
    # keyboard.add(types.KeyboardButton(text="Запросить погоду", request_location=True))
    # await message.answer("Привет напиши мне название города, я пришлю тебе сводку к погоду!", reply_markup=keyboard)




@dp.message_handler(lambda message: message.text == "auth", state=Form.waiting_for_action)
async def handle_button_click(message: types.Message, state: FSMContext):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    # KeyboardButton(text="Запросить погоду", request_location=True))
    await message.answer(f"Начнем Авторизацию!\nВведите свой логин")

    await state.finish()  # Завершаем состояние, удаляем клавиатуру
    await FSMauth.login.set()




@dp.message_handler(state=FSMauth.login)
async def ask_name(message: types.Message , state: FSMContext):
    # Задаем первый вопрос
    async with state.proxy() as data:
        data['login']=message.text
    await FSMauth.next()
    await message.answer("Введите свой пароль")
    # Отправляем вопрос пользователю

@dp.message_handler(state=FSMauth.passw)
async def ask_age(message: types.Message , state: FSMContext):
    # Задаем первый вопрос
    async with state.proxy() as data:
        data['passw']=message.text
    async with state.proxy() as data:
        await message.reply(str(data))
        print('st')
        auth(data['login'],data['passw'])
        print('end')
    await state.finish()




def register_handlers_start_auth(dp : Dispatcher):
    dp.register_message_handler(start , commands=['start','help'])
    dp.handle_button_click(handle_button_click)
    # dp.handle_button_click(get_contact)

