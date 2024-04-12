from aiogram import executor
# from test_ques_reb import *
from create_bot import dp
import start_and_authorizathion,test_ques_reb

executor.start_polling(dp, skip_updates=True)