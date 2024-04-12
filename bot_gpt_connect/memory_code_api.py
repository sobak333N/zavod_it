import requests
import json

def auth(login , passw):
    print('start_auth')
    url = 'https://mc.dev.rand.agency/api/v1/get-access-token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
    }

    data = {
        "email": login ,
        "password": passw,
        "device": "bot-v0.0.1"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print('Успешный запрос!')
        print('Ответ сервера:', response.json())
    else:
        print('Ошибка при выполнении запроса:')
        print('Статус код:', response.status_code)
        print('Текст ошибки:', response.text)