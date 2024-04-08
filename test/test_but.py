import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor

API_TOKEN = '7015685401:AAFbBOl5IRl6DiEVMpseW8FVgXyIYUJpEew'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Предположим, что у вас есть функция get_user_buttons(user_id), которая возвращает список кнопок для пользователя
def get_user_buttons(user_id):
    # Здесь можно реализовать логику для получения кнопок из базы данных или другого источника
    # В данном примере возвращается статический список кнопок
    # (SELECT .... )
    return ['Кнопка 1', 'Кнопка 2', 'Кнопка 3']

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    buttons = get_user_buttons(user_id)

    keyboard = InlineKeyboardMarkup()
    for button_text in buttons:
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_text))

    await message.answer("Выберите одну из кнопок:", reply_markup=keyboard)

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали: {callback_query.data}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





