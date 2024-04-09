import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor

from YaGPT_API import YandexGPTApi
from pprint import pprint

API_TOKEN = '7015685401:AAFbBOl5IRl6DiEVMpseW8FVgXyIYUJpEew'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

questions_bio = ["О ком нужно написать текст (ФИО)?", "Год рождение человека", "Пару прикольных фактов о нем"]
#questions_epi = ["О ком нужно написать текст (ФИО)?", "Как он скончался?(", "Его любили?"]
for_gpt_quest = "Напиши биографию по следующим пунктам: "
i = len(questions_bio)

# Предположим, что у вас есть функция get_user_buttons(user_id), которая возвращает список кнопок для пользователя
def get_user_buttons(user_id):
    # Здесь можно реализовать логику для получения кнопок из базы данных или другого источника
    # В данном примере возвращается статический список кнопок
    # (SELECT .... )
    return ['Написать эпитафию', 'Написать биографию']

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    buttons = get_user_buttons(user_id)

    keyboard = InlineKeyboardMarkup()
    for button_text in buttons:
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_text))

    await message.answer(questions_bio[0])
    #await message.answer("Выберите одну из кнопок:", reply_markup=keyboard)


@dp.message_handler()
async def process_answer(message: types.Message):
    global for_gpt_quest
    global i# Добавляем эту строку для доступа к глобальной переменной answers
    for_gpt_quest += message.text + " "  # Добавляем новый ответ к предыдущему с пробелом

    #if len(for_gpt_quest.split()) < len(questions_bio):
    if i > 1:
        await message.answer(questions_bio[len(questions_bio) - i + 1])
        i -= 1
    else:
        gpt = YandexGPTApi(config="config.ini")
        letter = [{
            "role": "user",
            "text": for_gpt_quest
        }]
        summary = gpt.make_request(letter)
        await message.answer(summary)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



