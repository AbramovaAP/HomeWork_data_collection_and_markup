'''
Задачи 3 - 7:
3. Сценарий Foursquare
4. Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
5. Используйте API Foursquare для поиска заведений в указанной категории.
6. Получите название заведения, его адрес и рейтинг для каждого из них.
7. Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.
'''
import requests
import json


# Ваши учетные данные API
CLIENT_ID = 'HDRF2THJ1COQK3KWAIGTXLSHKGDT0NJAG1GPFE3RDC1305NZ'
CLIENT_SECRET = 'WKTQXAVBF1XRZMFT5HDRSXANPBOHXT30TDEAYJMWSWI1ZQAD'

# # Конечная точка API
url = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
city = input("Введите название города на английском языке: ")
category = input("Введите название интересующей Вас категории на английском языке (например: Park, Zoos, Museums и т.п.) : ")

params = {
    'limit': 10,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "near": city,
    "query": category,
    'fields': 'name,location,rating'
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3k7yJ03WxILTs1ywnzWK50WqnOFdwenU9ezfoQSI8Rcc="
}

# Отправка запроса API и получение ответа
response = requests.request("GET", url, params=params, headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API по URL: ", response.url)
else:
    print("Запрос API отклонен с кодом состояния:", response.status_code)


data = response.json()

establishments = []
for place in data['results']:
    place_name = place.get('name')
    place_address = place.get('location')['formatted_address']
    place_rating = place.get('rating') if 'rating' in place else "Рейтинг не определялся"
    establishments.append({'name': place_name, 'address': place_address, 'rating': place_rating})

for establishment in establishments:
        print(f"Название: {establishment['name']}")
        print(f"Адрес: {establishment['address']}")
        print(f"Рейтинг: {establishment['rating']}")
        print()

# От преподавателя:
# Проверка на наличие поля rating - правильно, полезно проверять и существование location