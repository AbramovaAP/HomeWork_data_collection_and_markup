'''
                    Домашняя работа к уроку № 3:
    Системы управления базами данных MongoDB и Кликхаус в Python

1. Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе. 
https://www.mongodb.com/ https://www.mongodb.com/products/compass

2. Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта 
с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.

3. Поэкспериментируйте с различными методами запросов.

4. Зарегистрируйтесь в ClickHouse.

5. Загрузите данные в ClickHouse и создайте таблицу для их хранения.
'''

# 2. Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта 
# с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.

import json
from pymongo import MongoClient

# Чтение данных из JSON файла
with open("books_toscrape.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# Проверка загрузки на примере первой записи
print(data[0])
#Вывод:
'''
{'Название': 'A Light in the Attic', 'Цена в фунтах стерлингов': '51.77', 'Количество в наличии': 22, 
'Описание': "It's hard to imagine a world without A Light in the Attic. This now-classic collection 
of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. 
Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and 
fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to 
imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from 
Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous 
and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still 
and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? 
RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you 
up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never 
sounded so good. ...more"}
'''

# Соединение с MongoDB
client = MongoClient('localhost', 27017)
db = client['my_books_database']

# Создание коллекции на основании данных из JSON файла
collection_name = "Список книг от 13-09-2024"
collection = db[collection_name]

# Очистка коллекции, если уже существует
collection.delete_many({})

# Вставка данных
for item in data:
    # Преобразование цены в число
    item['Цена в фунтах стерлингов'] = float(item['Цена в фунтах стерлингов'].replace('£', '').strip())
    collection.insert_one(item)

client.close()

# Установление связи с MongoDB
client = MongoClient('localhost', 27017)
db = client['my_books_database']
collection = db['Список книг от 13-09-2024']

# 3. Поэкспериментируйте с различными методами запросов.
# 3.1 Просмотр количества документов в коллекции
document_count = collection.count_documents({})
print("Количества документов в коллекции:", document_count)
#Вывод:
# Количества документов в коллекции: 1000

# 3.2 Запрос количества и названий книг, дороже 59 фунтов
query = {"Цена в фунтах стерлингов": {"$gt": 59.00}}

# Получение документов, соответствующих запросу
documents = collection.find(query)

print("Количество книг дороже 59 фунтов - ", collection.count_documents(query), ":")
#Вывод:
'''
Количество книг дороже 59 фунтов -  12 :
Название книги: Thomas Jefferson and the Tripoli Pirates: The Forgotten War That Changed American History
Название книги: The Gray Rhino: How to Recognize and Act on the Obvious Dangers We Ignore
Название книги: The Diary of a Young Girl
Название книги: Boar Island (Anna Pigeon #19)
Название книги: The Improbability of Love
Название книги: The Man Who Mistook His Wife for a Hat and Other Clinical Tales
Название книги: The Barefoot Contessa Cookbook
Название книги: Last One Home (New Beginnings #1)
Название книги: The Perfect Play (Play by Play #1)
Название книги: The Bone Hunters (Lexy Vaughan & Steven Macaulay #2)
Название книги: Life Without a Recipe
Название книги: Civilization and Its Discontents
'''

# Отображение названий книг
for document in documents:
    print("Название книги:", document['Название'])

# 3.3 Запрос для определения максимальной и минимальной цены книги в коллекции
pipeline = [
    {"$group": {"_id": None, "max_price": {"$max": "$Цена в фунтах стерлингов"}, "min_price": {"$min": "$Цена в фунтах стерлингов"}}}
]

# Применение конвеера
result = list(collection.aggregate(pipeline))

# Получение минимального и максимального значений
max_price = result[0]["max_price"]
min_price = result[0]["min_price"]

# Печать результатов
print("Минимальная цена:", min_price)
print("Максимальная цена:", max_price)
#Вывод:
'''
Минимальная цена: 10.0
Максимальная цена: 59.99
'''
